"""Audio + timeline for the January occasion Reels (Veo Lite clips + freeze frame). Timings follow the recordings."""
import json, sys, wave
import numpy as np
import build_audio as B
SR = B.SR
dur = lambda n: len(B.load(n)) / SR
CFG = {
  "ep":  dict(intro=("xco-ep1", "Ooh la la! On the sixth of January, French families share a special cake. Whoever finds the little lucky charm inside wears the crown! It's called..."), word="w-fr-galette", try_="co2", end="co3", clip=8.0),
  "rey": dict(intro=("xto-rey1", "Shh! Tonight the Three Kings ride their camels through Spain, and children leave their shoes out for presents! In Spanish we call them..."), word="w-es-reyes", try_="ty2", end="ty3", clip=6.0),
  "bef": dict(intro=("xlu-bef1", "Awooo! Look! On the night before the sixth of January, a kind old lady flies over Italy and leaves sweets for good children. Here she comes..."), word="w-it-befana", try_="lw2", end="lw3", clip=8.0),
  "kid": dict(intro=("xny-kid1", "Hooray! In Thailand, the second Saturday of January is a special day just for children, with games, treats and bubbles! We call it..."), word="w-th-wandek", try_="ny2", end="nc3", clip=8.0),
}
def build(k):
    c = CFG[k]; clips = []
    def put(name, at, text=None, gain=1.0):
        sig = B.load(name); clips.append(dict(name=name, start=round(at,3), dur=round(len(sig)/SR,3), text=text, gain=gain)); return at + len(sig)/SR
    e = put(c["intro"][0], 0.3, c["intro"][1])
    w1 = e + 0.35; e = put(c["word"], w1, None, 1.3)
    turn = e + 0.9; e = put(c["try_"], turn, "Now you try! Say it with me!")
    w2 = e + 0.3; e = put(c["word"], w2, None, 1.3)
    end = round(e + 1.6, 3); put(c["end"], end + 0.4, "Learn with us at nongchang.co.uk")
    total = round(end + 4.6, 2); N = int(SR*total)
    voice = np.zeros((N,2)); sfx = np.zeros((N,2))
    for cl in clips:
        sig = B.load(cl["name"]); B.add(voice, sig, cl["start"], gain=cl.pop("gain")); cl["env"] = B.envelope(sig)
    B.add(sfx, B.pop(0.25), w1 - 0.12); B.add(sfx, B.sparkle(0.16), w1 + 0.05)
    B.add(sfx, B.pop(0.22), w2 - 0.12); B.add(sfx, B.ding(0.14), w2 + dur(c["word"]) + 0.3)
    B.add(sfx, B.whoosh(), end - 0.25); B.add(sfx, B.sparkle(0.14), end + 0.1)
    mus = B.music(total)
    venv = np.abs(voice).max(axis=1); kk = int(0.08*SR); sm = np.convolve(venv, np.ones(kk)/kk, mode="same")
    mus *= (1 - 0.62*np.clip(sm/0.04, 0, 1))[:, None]
    mix = mus*0.8 + voice + sfx; mix /= max(1.0, np.abs(mix).max()/0.95)
    with wave.open(B.D + f"mix-x{k}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix*32767).astype(np.int16).tobytes())
    json.dump(dict(total=total, clipEnd=c["clip"], end=end, word=[round(w1,3), round(w2,3)], turn=round(turn,3), clips=clips), open(B.D + f"tl-x{k}.json", "w"))
    print(k, "total", total, "word", round(w1,2), "turn", round(turn,2))
for k in sys.argv[1:] or list(CFG): build(k)
