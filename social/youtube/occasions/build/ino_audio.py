"""Audio + timeline for the "Merry Christmas" snowy Shorts (Omni/Veo clips, 24 Nov 2026)."""
import json, sys, wave
import numpy as np
import build_audio as B

SR = B.SR
CFG = {
    "co": dict(gem="gem-xco", intro="xco1", try_="co2", end="co3", word="w-fr-xmas"),
    "ny": dict(gem="gem-xny", intro="xny1", try_="ny2", end="nc3", word="w-th-xmas"),
    "lu": dict(gem="gem-xlu", intro="xlu1", try_="lw2", end="lw3", word="w-it-xmas"),
    "to": dict(gem=None, intro="xto1", try_="ty2", end="ty3", word="w-es-xmas"),
    "le": dict(gem=None, intro="xle1", try_="le2", end="le3", word="w-en-xmas"),
    "ino": dict(gem=None, intro="xto-ino1", try_="ty2", end="ty3", word="w-es-ino"),
}
TOTAL, CLIP_END, END = 21.6, 7.8, 17.0
TURN, WORD2 = 11.1, 13.95

def build(k):
    c = CFG[k]; N = int(SR * TOTAL)
    voice = np.zeros((N, 2)); sfx = np.zeros((N, 2)); amb = np.zeros((N, 2))
    if c["gem"]:
        gem = B.load(c["gem"])[: int(SR * CLIP_END)]
        fade = int(0.4 * SR); gem[-fade:] *= np.linspace(1, 0, fade)
        B.add(amb, gem, 0.0, gain=0.3)
    clips = []
    def put(name, at, text=None, gain=1.0):
        sig = B.load(name); B.add(voice, sig, at, gain=gain)
        clips.append(dict(name=name, start=at, dur=round(len(sig) / SR, 3), text=text, env=B.envelope(sig)))
    intro = {"co": "Hop, hop, hop! Brrr, it's snowing! In France, at Christmas, we say...",
             "ny": "Wheee! A snow fountain! In Thailand, at Christmas, we say...",
             "lu": "Awooo! Look, the Christmas star! In Italy, at Christmas, we say...",
             "to": "Olé! Look at all the lights! In Spain, at Christmas, we say...",
             "le": "Wheee! I love rolling in the snow! In England, at Christmas, we say...",
             "ino": "Peekaboo! Did I surprise you? In Spain, on the 28th of December, we play funny tricks and shout..."}[k]
    put(c["intro"], 0.3, intro)
    word_at = 0.3 + len(B.load(c["intro"])) / SR + 0.35
    put(c["word"], word_at, None, 1.3)
    put(c["try_"], TURN, "Now you try! Say it with me!")
    put(c["word"], WORD2, None, 1.3)
    put(c["end"], END + 0.4, "Learn with us at nongchang.co.uk")
    B.add(sfx, B.pop(0.25), word_at - 0.12); B.add(sfx, B.sparkle(0.16), word_at + 0.05)
    B.add(sfx, B.pop(0.22), WORD2 - 0.12); B.add(sfx, B.ding(0.14), WORD2 + 2.3)
    B.add(sfx, B.whoosh(), END - 0.25); B.add(sfx, B.sparkle(0.14), END + 0.1)
    mus = B.music(TOTAL)
    venv = np.abs(voice).max(axis=1); kk = int(0.08 * SR)
    sm = np.convolve(venv, np.ones(kk) / kk, mode="same")
    mus *= (1 - 0.62 * np.clip(sm / 0.04, 0, 1))[:, None]
    # music comes in softly under the Gemini clip, full from the freeze frame
    ramp = np.clip((np.arange(N) / SR - 7.0) / 1.5, 0.45, 1.0)
    mix = mus * 0.8 * ramp[:, None] + amb + voice + sfx
    mix /= max(1.0, np.abs(mix).max() / 0.95)
    with wave.open(B.D + f"mix-x{k}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    json.dump(dict(total=TOTAL, clipEnd=CLIP_END, end=END, word=[word_at, WORD2], turn=TURN, clips=clips), open(B.D + f"tl-x{k}.json", "w"))
    print(k, "word at", round(word_at, 2))

for k in sys.argv[1:] or ["ino"]:
    build(k)
