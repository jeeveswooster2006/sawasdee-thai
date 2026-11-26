"""Batch 2 grown-up Shorts: timelines + mixes from specs.py (phrases and sayings)."""
import json, subprocess, sys
import numpy as np
from audiolib import load, env, music, add, SR, D, T
from specs import specs, FLAG

def build(key, s):
    clips = []; t = 2.9
    for it in s["items"]:
        v = load(it["path"]); d = len(v) / SR
        if it["kind"] == "saying":
            p1 = t + 0.8; reveal = p1 + d + 0.3; turn = reveal + 2.2; p2 = turn + 2.2; end = p2 + d + 0.8
        else:
            p1 = t + 0.55; reveal = None; turn = p1 + d + 0.35; p2 = turn + 2.0; end = p2 + d + 0.6
        clips.append(dict(native=it["native"], roman=it["roman"], en=it["en"], literal=it["literal"], kind=it["kind"], emoji=it["emoji"],
                          start=t, p1=p1, reveal=reveal, turn=turn, p2=p2, end=end, dur=d, env=env(v), path=it["path"]))
        t = end
    total = t + 4.2
    vo = np.zeros(int(SR * (total + 1)))
    for c in clips:
        v = load(c["path"]); add(vo, v, c["p1"]); add(vo, v, c["p2"])
    m = music(total)
    e = np.convolve(np.abs(vo), np.ones(int(SR * 0.12)) / int(SR * 0.12), mode="same")
    duck = 1 - 0.65 * np.clip(e / 0.05, 0, 1)
    duck = np.convolve(duck, np.ones(int(SR * 0.08)) / int(SR * 0.08), mode="same")
    tt = T(len(m)); fade = np.minimum(1, tt / 0.8) * np.clip((total - tt) / 1.6, 0, 1)
    mix = (vo + m * duck * fade)[: int(SR * total)]
    mix = mix / max(1.0, np.abs(mix).max() / 0.95)
    st = np.stack([mix, mix], axis=1).astype(np.float32)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", "-", D + f"mix-{key}.wav"], input=st.tobytes())
    tl = dict(key=key, lang=s["lang"], kind=s["kind"], flag=FLAG[s["lang"]], hook=s["hook"], sub=s["sub"], emoji=s["emoji"], clips=clips, outro=t, total=total)
    json.dump(tl, open(D + f"tl-{key}.json", "w"), ensure_ascii=False)
    print(key, round(total, 1))

all_ = specs()
for k in (sys.argv[1:] or all_):
    build(k, all_[k])
