"""Pierce learns hello: timeline + audio. Writes tl-pierce.json and mix-pierce.wav."""
import json, wave
import numpy as np
import build_audio as B

SR = B.SR
dur = lambda n: len(B.load(n)) / SR
LANGS = [
    dict(k="th", flag="🇹🇭 Thai", word="สวัสดี", rom="sa-wàt-dii", line="pi-th", wclip="w-th-hello", text="Hi Pierce! In Thai, we say..."),
    dict(k="fr", flag="🇫🇷 French", word="Bonjour !", rom="", line="pi-fr", wclip="w-fr-hello", text="Hi Pierce! In French, we say..."),
    dict(k="es", flag="🇪🇸 Spanish", word="¡Hola!", rom="", line="pi-es", wclip="w-es-hello", text="Hi Pierce! In Spanish, we say..."),
    dict(k="it", flag="🇮🇹 Italian", word="Buongiorno!", rom="", line="pi-it", wclip="w-it-hello", text="Hi Pierce! In Italian, we say..."),
    dict(k="en", flag="🇬🇧 English", word="Hello!", rom="", line="pi-en", wclip="w-en-hello", text="Hi Pierce! In English, we say..."),
]
clips = []; segs = []
def put(name, at, who, text=None, word=False):
    clips.append(dict(name=name, start=round(at, 3), dur=round(dur(name), 3), who=who, text=text, word=word)); return at + dur(name)

t = 0.0
e = put("pi-intro", 0.5, "th", "This is Pierce! Today he's learning to say hello in five languages!")
segs.append(dict(kind="intro", start=0.0, end=round(e + 0.5, 3))); t = e + 0.5
for i, L in enumerate(LANGS):
    s = t; e = put(L["line"], s + 0.25, L["k"], L["text"])
    w1 = e + 0.25; e = put(L["wclip"], w1, L["k"], word=True)
    w2 = e + 0.5; e = put(L["wclip"], w2, L["k"], word=True)
    end = max(s + 6.6, e + 0.45)
    segs.append(dict(kind="lang", clip=i + 1, start=round(s, 3), end=round(end, 3), w1=round(w1, 3), **{k: L[k] for k in ("k", "flag", "word", "rom")}))
    t = end
s = t; e = put("pi-end", s + 0.3, "th", "Well done, Pierce! Now you can say hello in five languages!")
end = max(s + 6.4, e + 0.6)
segs.append(dict(kind="group", clip=6, start=round(s, 3), end=round(end, 3), wave=round(e + 0.05, 3))); t = end
END = round(t, 3)
put("nc3", END + 0.4, "th", "Learn with us at nongchang.co.uk")
TOTAL = round(END + 4.8, 2)

N = int(SR * TOTAL); vb = np.zeros((N, 2)); sfx = np.zeros((N, 2))
for c in clips:
    sig = B.load(c["name"]); B.add(vb, sig, c["start"], gain=1.35 if c["word"] else 1.0)
    if c["word"]: B.add(sfx, B.pop(0.2), c["start"] - 0.12)
B.add(sfx, B.sparkle(), 0.05)
for sg in segs:
    B.add(sfx, B.whoosh(0.14), sg["start"] - 0.1)
    if sg["kind"] == "lang": B.add(sfx, B.sparkle(0.12), sg["w1"] + 0.1)
    if sg["kind"] == "group": B.add(sfx, B.ding(0.18), sg["wave"]); B.add(sfx, B.sparkle(0.16), sg["wave"] + 0.1)
B.add(sfx, B.whoosh(), END - 0.25); B.add(sfx, B.sparkle(0.14), END + 0.1)
mus = B.music(TOTAL)
venv = np.abs(vb).max(axis=1); k = int(0.08 * SR)
sm = np.convolve(venv, np.ones(k) / k, mode="same")
mus *= (1 - 0.62 * np.clip(sm / 0.04, 0, 1))[:, None]
mix = mus * 0.8 + vb + sfx
mix /= max(1.0, np.abs(mix).max() / 0.95)
with wave.open(B.D + "mix-pierce.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
json.dump(dict(total=TOTAL, end=END, segs=segs, clips=clips), open(B.D + "tl-pierce.json", "w"), ensure_ascii=False, indent=1)
print("total", TOTAL, "end", END); [print(s) for s in segs]
