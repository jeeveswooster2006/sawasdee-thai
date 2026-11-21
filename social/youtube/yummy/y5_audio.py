"""Audio + timeline for the combined "Yummy in 5" Short: intro, five eating clips, quick "your turn" round, end card."""
import json, wave
import numpy as np
import build_audio as B

SR = B.SR
KEYS = ["ny", "co", "to", "lu", "le"]          # Thai, French, Spanish, Italian, English
WORD = {"ny": "w-aroi", "co": "w-delicieux", "to": "w-delicioso", "lu": "w-buonissimo", "le": "w-delicious"}
I_END, SEG, W1, W2 = 7.0, 6.2, 2.4, 4.2
SEG0 = [I_END + SEG * i for i in range(5)]
FIN = SEG0[-1] + SEG                            # 38.0
TRY_AT = FIN + 0.3
RAPID = [FIN + 3.4 + 2.1 * i for i in range(5)]
END = RAPID[-1] + 2.2
TOTAL = END + 5.0

N = int(SR * TOTAL)
voice = np.zeros((N, 2)); sfx = np.zeros((N, 2)); amb = np.zeros((N, 2))
clips = []
def put(name, at, text=None, gain=1.0):
    sig = B.load(name); B.add(voice, sig, at, gain=gain)
    clips.append(dict(name=name, start=round(at, 3), dur=round(len(sig) / SR, 3), text=text))

put("y5a", 0.5, "Hi friends! How do you say yummy around the world? Let's taste with my friends!")
for i, k in enumerate(KEYS):
    s = SEG0[i]
    raw = __import__("subprocess").run(["ffmpeg", "-loglevel", "error", "-i", B.D + f"y5/amb-{k}.wav", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).astype(np.float64)[: int(SR * SEG)]
    f = int(0.25 * SR); a[:f] *= np.linspace(0, 1, f); a[-f:] *= np.linspace(1, 0, f)
    B.add(amb, a, s, gain=0.32)
    put(WORD[k], s + W1, None, 1.3); put(WORD[k], s + W2, None, 1.3)
    B.add(sfx, B.whoosh(0.16), s - 0.2)
    B.add(sfx, B.pop(0.25), s + W1 - 0.12); B.add(sfx, B.sparkle(0.15), s + W1 + 0.05)
put("ny2", TRY_AT, "Now you try! Say it with me!")
for i, k in enumerate(KEYS):
    put(WORD[k], RAPID[i] + 0.15, None, 1.3)
    B.add(sfx, B.pop(0.22), RAPID[i])
B.add(sfx, B.ding(0.16), RAPID[-1] + 1.9)
put("nc3", END + 0.4, "Learn with us at nongchang.co.uk")
B.add(sfx, B.sparkle(), 0.05); B.add(sfx, B.whoosh(), FIN - 0.2); B.add(sfx, B.whoosh(), END - 0.25); B.add(sfx, B.sparkle(0.14), END + 0.1)

mus = B.music(TOTAL)
venv = np.abs(voice).max(axis=1); kk = int(0.08 * SR)
sm = np.convolve(venv, np.ones(kk) / kk, mode="same")
duck = (1 - 0.62 * np.clip(sm / 0.04, 0, 1))[:, None]
mus *= duck; amb *= duck
t = np.arange(N) / SR
level = np.where((t > I_END) & (t < FIN), 0.55, 0.85)
level = np.convolve(level, np.ones(int(0.3 * SR)) / int(0.3 * SR), mode="same")
mix = mus * level[:, None] + amb + voice + sfx
mix /= max(1.0, np.abs(mix).max() / 0.95)
with wave.open(B.D + "mix-y5.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
json.dump(dict(total=TOTAL, iEnd=I_END, seg=SEG, seg0=SEG0, w1=W1, w2=W2, fin=FIN, rapid=RAPID, end=END, keys=KEYS, clips=clips), open(B.D + "tl-y5.json", "w"))
print("total", round(TOTAL, 2), "fin", FIN, "end", round(END, 2))
