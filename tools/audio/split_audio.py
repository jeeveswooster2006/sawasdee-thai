import json, re, subprocess, sys, os
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
groups = json.load(open('audio_groups.json', encoding='utf-8'))
os.makedirs('audio_out', exist_ok=True)

def silences(path, noise='-40dB', d=0.2):
    out = subprocess.run([FF, '-hide_banner', '-i', path, '-af', f'silencedetect=noise={noise}:d={d}', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    dur = float(re.search(r'Duration: (\d+):(\d+):([\d.]+)', out).group(3)) + 60*int(re.search(r'Duration: (\d+):(\d+)', out).group(2))
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
    if len(ends) < len(starts): ends.append(dur)
    return dur, list(zip(starts, ends))

report = {}
for gi in [int(a) for a in sys.argv[1:]]:
    g = groups[gi]; n = len(g['ids'])
    path = f'audio_raw/group{gi:02d}.mp3'
    dur, sil = silences(path)
    # interior gaps only (exclude leading/trailing silence)
    merged = []
    for s, e in sil:
        if merged and s - merged[-1][1] < 0.12:
            merged[-1] = (merged[-1][0], e)
        else:
            merged.append((s, e))
    sil = merged
    interior = [(s, e) for s, e in sil if s > 0.05 and e < dur - 0.05]
    if len(interior) < n - 1:
        report[gi] = {'ok': False, 'why': f'only {len(interior)} gaps for {n} items'}; continue
    ranked = sorted(interior, key=lambda x: x[1] - x[0], reverse=True)
    chosen = sorted(ranked[:n - 1])
    min_chosen = min(e - s for s, e in chosen)
    max_unchosen = max([e - s for s, e in ranked[n - 1:]] or [0])
    lead_end = sil[0][1] if sil and sil[0][0] <= 0.05 else 0.0
    tail_start = sil[-1][0] if sil and sil[-1][1] >= dur - 0.05 else dur
    bounds = [lead_end] + [x for s, e in chosen for x in (s, e)] + [tail_start]
    segs = [(bounds[2*k], bounds[2*k+1]) for k in range(n)]
    for wid, (a, b) in zip(g['ids'], segs):
        a2, b2 = max(0, a - 0.06), min(dur, b + 0.12)
        subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-i', path, '-ss', f'{a2:.3f}', '-to', f'{b2:.3f}',
                        '-ac', '1', '-ar', '44100', '-b:a', '96k', '-af', 'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,afade=t=in:d=0.015,areverse,afade=t=in:d=0.03,areverse',
                        f'audio_out/{wid}.mp3'], check=True)
    report[gi] = {'ok': True, 'n': n, 'margin': round(min_chosen / max(max_unchosen, 0.001), 2),
                  'min_gap': round(min_chosen, 2), 'max_other_gap': round(max_unchosen, 2),
                  'seg_lengths': [round(b - a, 2) for a, b in segs], 'segs': [(round(a,3), round(b,3)) for a, b in segs]}
print(json.dumps(report, ensure_ascii=False, indent=0))
