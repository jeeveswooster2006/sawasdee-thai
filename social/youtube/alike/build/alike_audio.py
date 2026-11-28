"""'Sounds alike!' Shorts: two words that sound almost the same. Writes tl-<id>.json and mix-<id>.wav.
Reuses existing recordings only (native words + Torito's stock lines)."""
import json, sys, wave
import numpy as np
import build_audio as B

SR = B.SR
dur = lambda n: len(B.load(n)) / SR

CFG = {
  "perro": dict(kind="alike", title="Sounds alike!", host="es", lang="🇪🇸 Spanish",
    hook=["Two Spanish words…", "one tiny difference! 👀"],
    a=dict(word="pero", mean="but", emo="🤔", tip="quick tap r", clip="w-pero", col="teal"),
    b=dict(word="perro", mean="dog", emo="🐶", tip="rolled rrr! 🌀", clip="w-perro", col="pink"),
    joke=dict(head="Roll the r, or…", good="Tengo un perro", goodm="I have a dog 🐶", bad="Tengo un pero", badm="I have a “but” 🤔😂"),
    guess=("to1", "Can you guess what this word means? Listen!"), ask="b",
    praise=("amz", "You're amazing!"),
    say=("r3", "Now say it with me!"),
    end=("ty3", "Learn with us at nongchang.co.uk")),
}


def build(sid):
    c = CFG[sid]; host = c["host"]; clips = []; m = {}
    def voice(name, at, text):
        clips.append(dict(name=name, start=round(at, 3), dur=round(dur(name), 3), who=host, text=text)); return at + dur(name)
    def word(key, at):
        n = c[key]["clip"]; clips.append(dict(name=n, start=round(at, 3), dur=round(dur(n), 3), who=host, text=None, word=True, key=key)); return at + dur(n)
    m["hook"] = [0.6, 1.9]
    m["a"] = 3.6; word("a", 3.95); word("a", 5.25)
    m["b"] = 6.6; word("b", 6.95); word("b", 8.25)
    m["joke"] = 9.7; m["jokeBad"] = 11.6
    g = 14.4; e = voice(c["guess"][0], g, c["guess"][1]); m["guess"] = g
    w = e + 0.35; m["gw"] = round(w, 3); e = word(c["ask"], w)
    w2 = e + 0.45; e = word(c["ask"], w2)
    m["choices"] = round(e + 0.25, 3)
    m["count"] = [round(e + 0.7 + i * 0.85, 3) for i in range(3)]
    m["reveal"] = round(m["count"][2] + 0.85, 3)
    e = voice(c["praise"][0], m["reveal"] + 0.25, c["praise"][1])
    e = word(c["ask"], e + 0.2)
    s = e + 0.6; m["say"] = round(s, 3); e = voice(c["say"][0], s, c["say"][1])
    t1 = e + 0.35; m["sayA"] = round(t1, 3); e = word("a", t1); m["turnA"] = round(e + 0.15, 3)
    t2 = e + 2.0; m["sayB"] = round(t2, 3); e = word("b", t2); m["turnB"] = round(e + 0.15, 3)
    end = round(e + 2.1, 3)
    voice(c["end"][0], end + 0.4, c["end"][1])
    total = round(end + 4.8, 2)
    N = int(SR * total); vb = np.zeros((N, 2)); sfx = np.zeros((N, 2))
    for cl in clips:
        sig = B.load(cl["name"]); B.add(vb, sig, cl["start"], gain=1.35 if cl.get("word") else 1.0)
        cl["env"] = B.envelope(sig)
        if cl.get("word"): B.add(sfx, B.pop(0.2), cl["start"] - 0.12)
    B.add(sfx, B.sparkle(), 0.05)
    for t in m["hook"]: B.add(sfx, B.pop(), t)
    B.add(sfx, B.whoosh(), m["a"] - 0.1); B.add(sfx, B.whoosh(), m["b"] - 0.1)
    B.add(sfx, B.ding(0.16), m["joke"] + 0.9); B.add(sfx, B.pop(), m["jokeBad"]); B.add(sfx, B.sparkle(0.14), m["jokeBad"] + 0.5)
    B.add(sfx, B.pop(), m["choices"]); B.add(sfx, B.pop(), m["choices"] + 0.25)
    for t in m["count"]: B.add(sfx, B.pluck(1046.5, 0.3, 0.14), t)
    B.add(sfx, B.ding(), m["reveal"]); B.add(sfx, B.sparkle(0.16), m["reveal"] + 0.1)
    B.add(sfx, B.ding(0.12), m["turnA"]); B.add(sfx, B.ding(0.12), m["turnB"])
    B.add(sfx, B.whoosh(), end - 0.25); B.add(sfx, B.sparkle(0.14), end + 0.1)
    mus = B.music(total)
    venv = np.abs(vb).max(axis=1); k = int(0.08 * SR)
    sm = np.convolve(venv, np.ones(k) / k, mode="same")
    mus *= (1 - 0.62 * np.clip(sm / 0.04, 0, 1))[:, None]
    mix = mus * 0.85 + vb + sfx
    mix /= max(1.0, np.abs(mix).max() / 0.95)
    with wave.open(B.D + f"mix-{sid}.wav", "wb") as wv:
        wv.setnchannels(2); wv.setsampwidth(2); wv.setframerate(SR); wv.writeframes((mix * 32767).astype(np.int16).tobytes())
    cfg = {k2: v for k2, v in c.items() if k2 not in ("guess", "praise", "say", "end")}
    json.dump(dict(id=sid, title=c["title"], total=total, end=end, clips=clips, marks=m, cfg=cfg), open(B.D + f"tl-{sid}.json", "w"), ensure_ascii=False)
    print(sid, "total", total, "end", end, {k: v for k, v in m.items()})


if __name__ == "__main__":
    for sid in sys.argv[1:] or list(CFG):
        build(sid)
