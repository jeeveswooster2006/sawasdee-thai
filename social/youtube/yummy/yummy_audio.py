"""Audio + timeline for the Gemini "Yummy!" Shorts (co = Coco/French, ny = Nong Chang/Thai)."""
import json, sys, wave
import numpy as np
import build_audio as B

SR = B.SR
CFG = {
    "co": dict(gem="gem-co", intro="co1", try_="co2", end="co3", word="w-delicieux"),
    "ny": dict(gem="gem-ny", intro="ny1", try_="ny2", end="nc3", word="w-aroi"),
    "lu": dict(gem="gem-lu", intro="lw1", try_="lw2", end="lw3", word="w-buonissimo"),
    "to": dict(gem="gem-to", intro="ty1", try_="ty2", end="ty3", word="w-delicioso"),
    "le": dict(gem="gem-le", intro="le1", try_="le2", end="le3", word="w-delicious"),
}
TOTAL, CLIP_END, END = 20.6, 10.0, 16.2

def build(k):
    c = CFG[k]; N = int(SR * TOTAL)
    voice = np.zeros((N, 2)); sfx = np.zeros((N, 2)); amb = np.zeros((N, 2))
    gem = B.load(c["gem"])[: int(SR * (6.4 if k in ("to", "le") else CLIP_END))]
    fade = int(0.4 * SR); gem[-fade:] *= np.linspace(1, 0, fade)
    B.add(amb, gem, 0.0, gain=0.35)
    clips = []
    def put(name, at, text=None, gain=1.0):
        sig = B.load(name); B.add(voice, sig, at, gain=gain)
        clips.append(dict(name=name, start=at, dur=round(len(sig) / SR, 3), text=text, env=B.envelope(sig)))
    intro = {"co": "Ooh la la! A warm croissant! In France, when food is yummy, we say...",
             "ny": "Mmm, mango sticky rice! In Thailand, when food is yummy, we say...",
             "lu": "Mmm, a cheesy pizza! In Italy, when food is yummy, we say...",
             "to": "Mmm, churros with hot chocolate! In Spain, when food is yummy, we say...",
             "le": "Mmm, a scone with jam and cream! In England, when food is yummy, we say..."}[k]
    put(c["intro"], 0.4, intro)
    word_at = 0.4 + len(B.load(c["intro"])) / SR + 0.35
    put(c["word"], word_at, None, 1.3)
    put(c["try_"], 10.3, "Now you try! Say it with me!")
    put(c["word"], 13.4, None, 1.3)
    put(c["end"], END + 0.4, "Learn with us at nongchang.co.uk")
    B.add(sfx, B.pop(0.25), word_at - 0.12); B.add(sfx, B.sparkle(0.16), word_at + 0.05)
    B.add(sfx, B.pop(0.22), 13.28); B.add(sfx, B.ding(0.14), 15.0)
    B.add(sfx, B.whoosh(), END - 0.25); B.add(sfx, B.sparkle(0.14), END + 0.1)
    mus = B.music(TOTAL)
    venv = np.abs(voice).max(axis=1); kk = int(0.08 * SR)
    sm = np.convolve(venv, np.ones(kk) / kk, mode="same")
    mus *= (1 - 0.62 * np.clip(sm / 0.04, 0, 1))[:, None]
    # music comes in softly under the Gemini clip, full from the freeze frame
    ramp = np.clip((np.arange(N) / SR - 8.5) / 1.5, 0.35, 1.0)
    mix = mus * 0.8 * ramp[:, None] + amb + voice + sfx
    mix /= max(1.0, np.abs(mix).max() / 0.95)
    with wave.open(B.D + f"mix-{k}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    json.dump(dict(total=TOTAL, clipEnd=CLIP_END, end=END, word=[word_at, 13.4], clips=clips), open(B.D + f"tl-{k}.json", "w"))
    print(k, "word at", round(word_at, 2))

for k in sys.argv[1:] or ["co", "ny"]:
    build(k)
