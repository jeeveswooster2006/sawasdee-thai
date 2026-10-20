"""Spanish copy of ../split_audio.py (letter-count lengths, shorter pauses allowed).

Split each batch clip in audio_raw/ into one mp3 per word in audio_out/.

Boundaries are chosen by dynamic programming over the detected silences: it rewards
cutting at long gaps and penalises segments whose speech length is far from what the
word's Thai text length predicts. That stops a long phrase with an internal pause
(e.g. รักวัวให้ผูก รักลูกให้ตี) being split in two, and catches short gaps between words.
Usage: python3 split_audio.py 0 1 2 ...   (batch numbers from audio_groups.json)
"""
import json, math, re, subprocess, sys, os
try:
    import imageio_ffmpeg
    FF = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FF = 'ffmpeg'
groups = json.load(open('audio_groups.json', encoding='utf-8'))
NOISE, MIN_GAP = os.environ.get('NOISE', '-40dB'), float(os.environ.get('MIN_GAP', '0.12'))
LAMBDA = 0.6


def silences(path, noise=None, d=None):
    noise, d = noise or NOISE, d or MIN_GAP
    out = subprocess.run([FF, '-hide_banner', '-i', path, '-af', f'silencedetect=noise={noise}:d={d}', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    h, m, s = re.search(r'Duration: (\d+):(\d+):([\d.]+)', out).groups()
    dur = int(h) * 3600 + int(m) * 60 + float(s)
    starts = [float(x) for x in re.findall(r'silence_start: ([\d.]+)', out)]
    ends = [float(x) for x in re.findall(r'silence_end: ([\d.]+)', out)]
    if len(ends) < len(starts): ends.append(dur)
    merged = []
    for a, b in zip(starts, ends):
        if merged and a - merged[-1][1] < 0.12:   # a click inside a pause: treat as one pause
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return dur, merged


def thai_len(t):
    """Spoken length estimate: letters only (Spanish)."""
    return max(1, len(re.sub(r'[^\w]', '', t)))


def align(path, texts):
    dur, sil = silences(path)
    lead = sil[0][1] if sil and sil[0][0] <= 0.05 else 0.0
    tail = sil[-1][0] if sil and sil[-1][1] >= dur - 0.05 else dur
    gaps = [(a, b) for a, b in sil if a > 0.05 and b < dur - 0.05]
    n, G = len(texts), len(gaps)
    if G < n - 1:
        raise ValueError(f'only {G} gaps for {n} items')
    lens = [thai_len(t) for t in texts]
    speech_total = (tail - lead) - sum(b - a for a, b in gaps)
    med_gap = sorted(b - a for a, b in gaps)[G // 2]
    start = lambda j: lead if j == -1 else gaps[j][1]
    end = lambda j: tail if j == G else gaps[j][0]
    prev, back = {-1: 0.0}, [dict() for _ in range(n + 1)]
    for k in range(1, n + 1):
        cur, share = {}, lens[k - 1] / sum(lens)
        for j in ([G] if k == n else range(G)):
            best = None
            for i, sc in prev.items():
                if i >= j: continue
                speech = end(j) - start(i) - sum(gaps[t][1] - gaps[t][0] for t in range(i + 1, j))
                if speech <= 0.05: continue
                v = sc + (0 if j == G else (gaps[j][1] - gaps[j][0]) / med_gap) \
                    - LAMBDA * math.log(speech / (share * speech_total)) ** 2
                if best is None or v > best[0]: best = (v, i)
            if best: cur[j], back[k][j] = best
        prev = cur
    segs, j = [], G
    for k in range(n, 0, -1):
        i = back[k][j]; segs.append((start(i), end(j))); j = i
    return dur, segs[::-1]


if __name__ == '__main__':
    os.makedirs('audio_out', exist_ok=True)
    report = {}
    for gi in [int(a) for a in sys.argv[1:]]:
        g = groups[gi]
        path = f'audio_raw/group{gi:02d}.mp3'
        try:
            dur, segs = align(path, g['texts'])
        except ValueError as e:
            report[gi] = {'ok': False, 'why': str(e)}; continue
        for wid, (a, b) in zip(g['ids'], segs):
            a2, b2 = max(0, a - 0.06), min(dur, b + 0.12)
            subprocess.run([FF, '-hide_banner', '-loglevel', 'error', '-y', '-i', path, '-ss', f'{a2:.3f}', '-to', f'{b2:.3f}',
                            '-ac', '1', '-ar', '44100', '-b:a', '96k', '-af',
                            'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.04,areverse,'
                            'silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse,'
                            'afade=t=in:d=0.015,areverse,afade=t=in:d=0.03,areverse',
                            f'audio_out/{wid}.mp3'], check=True)
        report[gi] = {'ok': True, 'n': len(segs), 'segs': [(round(a, 3), round(b, 3)) for a, b in segs]}
    print(json.dumps(report, ensure_ascii=False))
