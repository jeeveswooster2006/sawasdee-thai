"""Holiday phrases Shorts (grown-ups, not made for kids): timeline + mix. Native recordings, a 'your turn' pause,
a soft warm music bed ducked under every phrase. Writes tl-<key>.json and mix-<key>.wav (48 kHz stereo)."""
import json, subprocess
import numpy as np
SR = 48000
D = "/tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/holiday/"
C = "/home/user/sawasdee-thai/"
rng = np.random.default_rng(7)
T = lambda n: np.arange(n) / SR

OLD_SHORTS = {
  "th-restaurant": dict(lang="th", flag="🇹🇭", hook="Eating out in Thailand?", sub="4 Thai phrases you'll use at every meal", emoji="🍜", phrases=[
    ("audio/res-l1-0.mp3", "ขอเมนู", "khɔ̌ɔ mee-nuu", "Menu, please", "📋"),
    ("audio/res-l1-2.mp3", "ไม่เผ็ด", "mâi phèt", "Not spicy", "🌶️"),
    ("audio/res-l1-5.mp3", "อร่อยมาก", "à-ròi mâak", "Very delicious!", "😋"),
    ("audio/res-l1-4.mp3", "เก็บเงินด้วย", "kèp ngən dûai", "The bill, please", "🧾")]),
  "fr-restaurant": dict(lang="fr", flag="🇫🇷", hook="Eating out in France?", sub="4 French phrases you'll use at every meal", emoji="🥐", phrases=[
    ("courses/fr/audio/fr-res-l1-0.mp3", "la carte", "", "The menu", "📋"),
    ("courses/fr/audio/fr-phr-l1-1.mp3", "je voudrais…", "", "I would like…", "🙋"),
    ("courses/fr/audio/fr-res-l1-4.mp3", "C'est délicieux !", "", "It's delicious!", "😋"),
    ("courses/fr/audio/fr-res-l1-5.mp3", "L'addition, s'il vous plaît", "", "The bill, please", "🧾")]),
  "es-restaurant": dict(lang="es", flag="🇪🇸", hook="Eating out in Spain?", sub="4 Spanish phrases you'll use at every meal", emoji="🥘", phrases=[
    ("courses/es/audio/es-res-l1-0.mp3", "la carta", "", "The menu", "📋"),
    ("courses/es/audio/es-phr-l1-0.mp3", "por favor", "", "Please", "🙏"),
    ("courses/es/audio/es-res-l1-4.mp3", "¡Está buenísimo!", "", "It's delicious!", "😋"),
    ("courses/es/audio/es-res-l1-5.mp3", "La cuenta, por favor", "", "The bill, please", "🧾")]),
  "it-restaurant": dict(lang="it", flag="🇮🇹", hook="Eating out in Italy?", sub="4 Italian phrases you'll use at every meal", emoji="🍝", phrases=[
    ("courses/it/audio/it-res-l1-0.mp3", "il menù", "", "The menu", "📋"),
    ("courses/it/audio/it-phr-l1-1.mp3", "vorrei…", "", "I would like…", "🙋"),
    ("courses/it/audio/it-res-l1-4.mp3", "È buonissimo!", "", "It's delicious!", "😋"),
    ("courses/it/audio/it-res-l1-5.mp3", "Il conto, per favore", "", "The bill, please", "🧾")]),
}

def load(path):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", C + path, "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    x = np.frombuffer(raw, dtype=np.float32).astype(np.float64)
    # trim leading/trailing silence
    a = np.abs(x); th = a.max() * 0.03
    idx = np.where(a > th)[0]
    x = x[max(0, idx[0] - 800): idx[-1] + 2400] if len(idx) else x
    return x / (np.abs(x).max() + 1e-9) * 0.82

def env(sig, fps=30):
    hop = SR // fps; n = len(sig) // hop + 1
    e = np.array([np.sqrt(np.mean(sig[i*hop:(i+1)*hop] ** 2)) if len(sig[i*hop:(i+1)*hop]) else 0 for i in range(n)])
    return (e / (e.max() + 1e-9)).round(3).tolist()

# ---------- a soft, warm music bed (92 bpm, gentle keys, sub bass, brushed beat) ----------
BPM = 92; BEAT = 60 / BPM
def note(m): return 440 * 2 ** ((m - 69) / 12)
def keys(f, d, amp):
    n = int(SR * d); t = T(n)
    s = sum((0.5 ** k) * np.sin(2 * np.pi * f * (k + 1) * t + 0.3 * k) * np.exp(-t * (2.2 + 1.5 * k)) for k in range(4))
    return amp * s * (1 - np.exp(-t * 900)) * np.minimum(1, (d - t) / 0.05)
def pad(f, d, amp):
    n = int(SR * d); t = T(n)
    s = np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.003 * t) + 0.25 * np.sin(2 * np.pi * f * 0.5 * t)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    return amp * s * a
def kick(amp=0.28):
    n = int(SR * 0.2); t = T(n)
    return amp * np.sin(2 * np.pi * (48 + 70 * np.exp(-t * 28)) * t) * np.exp(-t * 14)
def brush(amp=0.03):
    n = int(SR * 0.12); t = T(n)
    return amp * rng.standard_normal(n) * np.exp(-t * 40)
def add(buf, x, at):
    i = int(at * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]; buf[i:i + len(x)] += x

PROG = [(60, [60, 64, 67, 71]), (57, [57, 60, 64, 67]), (53, [53, 57, 60, 64]), (55, [55, 59, 62, 65])]  # Cmaj7 Am7 Fmaj7 G7
def music(total):
    b = np.zeros(int(SR * (total + 1)))
    bar = BEAT * 4; t = 0.0; k = 0
    while t < total:
        root, ch = PROG[k % 4]
        for m in ch: add(b, pad(note(m), bar + 0.3, 0.018), t)
        add(b, keys(note(root - 24), bar * 0.9, 0.09), t)
        for j, m in enumerate([ch[0] + 12, ch[2] + 12, ch[1] + 12, ch[3] + 12]):
            add(b, keys(note(m), 0.9, 0.035), t + j * BEAT + (BEAT / 2 if j % 2 else 0))
        for j in range(4):
            if j in (0, 2): add(b, kick(), t + j * BEAT)
            add(b, brush(0.025), t + j * BEAT + BEAT / 2)
        t += bar; k += 1
    return b

