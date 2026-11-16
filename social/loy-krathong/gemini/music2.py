"""Music bed + voices + little effects for the Loy Krathong clip. Writes mix.wav (48 kHz stereo)."""
import json, subprocess
import numpy as np

SR = 48000
DUR = 39.7
N = int(SR * DUR)
rng = np.random.default_rng(3)
D = "/tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/loy/"
G = "/tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/loyg/"

def t_(n):
    return np.arange(n) / SR

def ranat(freq, dur=1.1, amp=0.25):
    """Wooden xylophone (ranat ek) style: bright strike, quick decay, slightly inharmonic overtones."""
    n = int(SR * dur); t = t_(n)
    env = np.exp(-t * 5.5) * (1 - np.exp(-t * 900))
    s = np.sin(2 * np.pi * freq * t) + 0.45 * np.sin(2 * np.pi * freq * 3.98 * t) * np.exp(-t * 14) + 0.2 * np.sin(2 * np.pi * freq * 9.1 * t) * np.exp(-t * 30)
    return amp * s * env

def ching(dur=1.6, amp=0.07, open_=True):
    """Small Thai finger cymbals: inharmonic metallic partials; 'chap' is the damped stroke."""
    n = int(SR * dur); t = t_(n)
    parts = [2860, 3420, 4210, 5170, 6630, 7900]
    s = sum(np.sin(2 * np.pi * f * t + rng.random() * 6) / (i + 1) ** 0.4 for i, f in enumerate(parts))
    env = np.exp(-t * (2.2 if open_ else 22)) * (1 - np.exp(-t * 3000))
    return amp * s * env

def pad(freqs, dur, amp=0.05):
    n = int(SR * dur); t = t_(n)
    s = sum(np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.21 * t + i)) for i, f in enumerate(freqs))
    s += 0.3 * sum(np.sin(2 * np.pi * f * 2.003 * t) for f in freqs)
    env = np.minimum(1, t / 2.5) * np.minimum(1, (dur - t) / 2.5)
    return amp * s * env / len(freqs)

def add(buf, sig, at, pan=0.0):
    i = int(at * SR)
    if i >= len(buf): return
    sig = sig[: len(buf) - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(sig), 0] += sig * l
    buf[i:i + len(sig), 1] += sig * r

music = np.zeros((N, 2))
# five-note scale on C (C D E G A), as in much Thai folk music
base = 261.63
scale = [0, 2, 4, 7, 9, 12, 14, 16, 19, 21]
f = lambda deg, octv=0: base * 2 ** ((scale[deg] + 12 * octv) / 12)
BEAT = 60 / 88
phrase = [  # (beat, degree)
    (0, 4), (1, 3), (1.5, 4), (2, 5), (3, 4), (4, 2), (5, 3), (5.5, 2), (6, 1), (7, 0),
    (8, 2), (9, 3), (9.5, 4), (10, 5), (11, 7), (12, 6), (13, 5), (13.5, 4), (14, 3), (15, 2),
]
start = 0.25
loop_beats = 16
nb = int((33.7 - start) / BEAT)
for b in range(0, nb, loop_beats):
    for (bt, deg) in phrase:
        at = start + (b + bt) * BEAT
        if at < 33.7:
            add(music, ranat(f(deg), amp=0.16), at, pan=-0.25)
            add(music, ranat(f(deg) * 2, dur=0.6, amp=0.045), at + 0.012, pan=0.35)  # higher ranat echo
# soft low "khong" pulses on bar starts
for b in range(0, nb, 4):
    at = start + b * BEAT
    add(music, ranat(f(0) / 2, dur=1.8, amp=0.10), at, pan=0)
# ching (open) on beat 2, chap (closed) on beat 4 of each bar
for b in range(0, nb):
    at = start + b * BEAT
    if b % 4 == 1: add(music, ching(open_=True), at, pan=0.3)
    if b % 4 == 3: add(music, ching(dur=0.3, amp=0.05, open_=False), at, pan=0.3)
# warm drone
add(music, pad([f(0, -1), f(3, -1), f(0)], 34.4, amp=0.07), 0.0)
# ending: a gentle rising run and a held chord under the end card
for i, deg in enumerate([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
    add(music, ranat(f(deg), dur=1.6, amp=0.13), 33.8 + i * 0.07, pan=-0.5 + i * 0.1)
add(music, pad([f(0), f(2), f(4), f(0, 1)], 5.9, amp=0.09), 33.8)
add(music, ching(dur=3.0, amp=0.08), 33.8, pan=0.0)
add(music, ching(dur=3.0, amp=0.06), 35.4, pan=-0.2)

# --- effects ---
fx = np.zeros((N, 2))
def chime(at, notes=(9, 7, 5), amp=0.10):
    for i, d in enumerate(notes):
        n = int(SR * 1.4); t = t_(n)
        s = np.sin(2 * np.pi * f(d, 1) * t) * np.exp(-t * 3.5) + 0.3 * np.sin(2 * np.pi * f(d, 2) * t) * np.exp(-t * 6)
        add(fx, amp * s, at + i * 0.09, pan=0.2 - i * 0.2)
def plop(at, amp=0.25):
    n = int(SR * 0.35); t = t_(n)
    fr = 900 * np.exp(-t * 14) + 180
    s = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-t * 16)
    noise = rng.standard_normal(n) * np.exp(-t * 30) * 0.15
    add(fx, amp * (s + noise), at)
chime(20.3, (4, 6, 8), 0.09)    # word card
chime(26.6, (6, 8, 9), 0.07)    # "Loy Krathong!"

# --- voices ---
def load(path):
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", path, "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.int16).astype(np.float64) / 32768

L = json.load(open(D + "lines.json"))
voice = np.zeros((N, 2))
for at, path in [(0.8, "voice/l1a.mp3"), (7.0, "voice/l2a.mp3"), (13.9, "voice/l3a.mp3"), (22.6, "v2/l4b.mp3")]:
    add(voice, load(D + path) * 0.95, at)
th = load(D + "voice/th_a.mp3")
add(voice, th * 0.95, 20.8)
add(voice, th * 0.95, 28.0)
# Gemini clip sound (water, crowd, fireworks), crossfaded like the pictures
amb = np.zeros((N, 2))
for at, name in [(0.0, "clip4"), (9.4, "clip3"), (18.8, "clip2"), (28.2, "clip1")]:
    raw = subprocess.run(["ffmpeg", "-v", "quiet", "-i", G + "in/" + name + ".mp4", "-vn", "-f", "s16le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True).stdout
    a = np.frombuffer(raw, dtype=np.int16).astype(np.float64).reshape(-1, 2) / 32768
    a = a[: int(SR * 10.0)]
    fl = int(SR * 0.6); ramp = np.linspace(0, 1, fl)[:, None]
    if at > 0: a[:fl] *= ramp
    a[-fl:] *= ramp[::-1]
    i = int(at * SR); a = a[: N - i]; amb[i:i + len(a)] += a
# duck the music under speech
env = np.abs(voice).max(axis=1)
k = int(SR * 0.25)
def mavg(x, k):
    c = np.cumsum(np.concatenate([[0.0], x])); y = (c[k:] - c[:-k]) / k
    pad = len(x) - len(y); return np.concatenate([np.full(pad // 2, y[0]), y, np.full(pad - pad // 2, y[-1])])
sm = mavg(env, k)
duck = 1 - 0.62 * np.clip(sm / 0.05, 0, 1)
duck = mavg(duck, k)
mix = (music + 0.38 * amb) * duck[:, None] + fx + voice
# fade out
fo = int(SR * 1.2)
mix[-fo:] *= np.linspace(1, 0, fo)[:, None]
mix /= max(1e-9, np.abs(mix).max()) / 0.89
out = (mix * 32767).astype(np.int16)
import wave
with wave.open(G + "mix.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(out.tobytes())
print("ok", out.shape)
