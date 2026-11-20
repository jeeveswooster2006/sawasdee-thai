"""Timelines + audio for the three pilot Shorts. Writes tl-<n>.json (for the scene) and mix-<n>.wav (48 kHz stereo).
Bright, happy: a bouncy ukulele-ish bed at 124 bpm, ducked under every voice, plus pops, dings and sparkles."""
import json, subprocess, sys
import numpy as np

SR = 48000
D = "/tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/shorts/"
rng = np.random.default_rng(11)
T = lambda n: np.arange(n) / SR


def load(name):
    raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", D + "snd/" + name + ".wav", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
    return np.frombuffer(raw, dtype=np.float32).astype(np.float64)


def dur(name):
    return len(load(name)) / SR


# ---------- timelines (seconds) ----------
# clip: (name, start, who)  who = speaker key for the bouncing mascot / caption
SHORTS = {
    1: dict(title="Say it in 5!", end=20.9, total=25.6, clips=[
        ("nc1", 0.5, "th", "Hi friends! How do you say thank you? Let's ask my friends!"),
        ("w-th", 5.9, "th", None), ("w-fr", 7.9, "fr", None), ("w-es", 9.9, "es", None), ("w-it", 11.9, "it", None), ("w-en", 13.9, "en", None),
        ("nc2", 16.1, "th", "Now you try! Say thank you in your favourite language!"),
        ("nc3", 21.3, "th", "Learn with us at nongchang.co.uk"),
    ]),
    2: dict(title="Guess the word!", end=19.0, total=23.6, clips=[
        ("to1", 0.5, "es", "Can you guess what this word means? Listen!"),
        ("w-manzana", 3.8, "es", None), ("w-manzana", 5.3, "es", None),
        ("to2", 6.9, "es", "Is it a banana... an apple... or a cat?"),
        ("to3", 13.6, "es", "It's an apple! Yay! You're amazing!"),
        ("w-manzana", 17.5, "es", None),
        ("to4", 19.4, "es", "Play more at nongchang.co.uk"),
    ]),
    3: dict(title="Funny sayings!", end=22.4, total=27.0, clips=[
        ("lu1", 0.5, "it", "Hi, I'm Lupo! When Italians are super, super hungry, they say..."),
        ("w-lupi", 6.5, "it", None),
        ("lu2", 9.0, "it", "That means... to have a hunger like wolves! Like me! Awooo!"),
        ("lu3", 16.0, "it", "Now say it with me!"),
        ("w-lupi", 17.8, "it", None),
        ("lu4", 22.8, "it", "Find more funny sayings at nongchang.co.uk"),
    ]),
}
# extra marks used by the scene (absolute seconds)
MARKS = {
    2: dict(banana=6.9 + 0.46, apple=6.9 + 1.76, cat=6.9 + 3.0, three=6.9 + 3.92, two=6.9 + 4.74, one=6.9 + 5.74, reveal=13.45),
    3: dict(words=[0.0, 0.48, 0.78, 1.22, 1.42], turn=20.0),
}


def envelope(sig, fps=30):
    hop = SR // fps
    n = len(sig) // hop + 1
    e = np.array([np.sqrt(np.mean(sig[i * hop:(i + 1) * hop] ** 2)) if len(sig[i * hop:(i + 1) * hop]) else 0 for i in range(n)])
    return (e / (e.max() + 1e-9)).round(3).tolist()


# ---------- instruments ----------
def pluck(f, d=0.45, amp=0.12):
    n = int(SR * d); t = T(n)
    s = sum((0.6 ** k) * np.sin(2 * np.pi * f * (k + 1) * t) * np.exp(-t * (6 + 4 * k)) for k in range(5))
    return amp * s * (1 - np.exp(-t * 3000))


def bass(f, d=0.4, amp=0.2):
    n = int(SR * d); t = T(n)
    return amp * (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)) * np.exp(-t * 3) * (1 - np.exp(-t * 500)) * np.minimum(1, (d - t) / 0.02)


def kick(amp=0.45):
    n = int(SR * 0.22); t = T(n)
    return amp * np.sin(2 * np.pi * (50 + 110 * np.exp(-t * 30)) * t) * np.exp(-t * 16)


def clap(amp=0.16):
    n = int(SR * 0.16); t = T(n)
    return amp * rng.standard_normal(n) * np.exp(-t * 30) * (1 + 0.6 * np.sin(2 * np.pi * 1300 * t))


def shaker(amp=0.035):
    n = int(SR * 0.06); t = T(n)
    return amp * rng.standard_normal(n) * np.exp(-t * 70)


def pop(amp=0.32):
    n = int(SR * 0.14); t = T(n)
    return amp * np.sin(2 * np.pi * (500 + 900 * t / 0.14) * t) * np.exp(-t * 28)


def ding(amp=0.22):
    n = int(SR * 1.3); t = T(n)
    return amp * sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in [(1318.5, 1, 3), (1975.5, 0.5, 4), (2637, 0.3, 6)])


def sparkle(amp=0.12):
    out = np.zeros(int(SR * 0.9))
    for i, f in enumerate([1568, 1976, 2349, 2637, 3136, 3951]):
        s = pluck(f, 0.4, amp * 0.6)
        j = int(i * 0.07 * SR); out[j:j + len(s)] += s[: len(out) - j]
    return out


def whoosh(amp=0.18):
    n = int(SR * 0.5); t = T(n)
    return amp * rng.standard_normal(n) * np.sin(np.pi * t / 0.5) ** 2 * (0.4 + t)


def add(buf, sig, at, pan=0.0, gain=1.0):
    i = int(at * SR)
    if i < 0 or i >= len(buf): return
    sig = sig[: len(buf) - i] * gain
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(sig), 0] += sig * l * 1.414
    buf[i:i + len(sig), 1] += sig * r * 1.414


# C – G – Am – F, bright and simple
CHORDS = [[261.6, 329.6, 392.0], [196.0, 246.9, 293.7], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6]]
ROOTS = [65.4, 49.0, 55.0, 43.65]


def music(total):
    N = int(SR * total); m = np.zeros((N, 2))
    beat = 60 / 124
    b = 0
    while b * beat < total - 0.6:
        t0 = b * beat; bar = (b // 4) % 4; ch = CHORDS[bar]
        if b % 4 in (0, 2): add(m, kick(), t0)
        if b % 4 in (1, 3): add(m, clap(), t0)
        for k in range(2): add(m, shaker(), t0 + k * beat / 2, pan=0.4)
        add(m, bass(ROOTS[bar] * 2), t0, gain=1.0 if b % 2 == 0 else 0.7)
        # ukulele strum pattern: down on beat, up on the "and"
        for k, f in enumerate(ch):
            add(m, pluck(f * 2, 0.35, 0.05), t0 + k * 0.012, pan=-0.3)
            add(m, pluck(f * 2, 0.3, 0.035), t0 + beat / 2 + k * 0.012, pan=0.3)
        # little bell melody every other bar
        if (b // 4) % 2 == 1 and b % 4 in (0, 2):
            add(m, pluck(ch[(b // 2) % 3] * 4, 0.5, 0.05), t0 + beat / 4, pan=0.2)
        b += 1
    fade = int(0.8 * SR)
    m[-fade:] *= np.linspace(1, 0, fade)[:, None]
    return m


def build(n):
    cfg = SHORTS[n]; total = cfg["total"]; N = int(SR * total)
    voice = np.zeros((N, 2)); sfx = np.zeros((N, 2))
    clips = []
    for name, start, who, text in cfg["clips"]:
        sig = load(name)
        g = 1.25 if name.startswith("w-") else 1.0
        add(voice, sig, start, gain=g)
        clips.append(dict(name=name, start=start, dur=round(len(sig) / SR, 3), who=who, text=text, env=envelope(sig)))
        if name.startswith("w-"): add(sfx, pop(0.22), start - 0.12)
    add(sfx, sparkle(), 0.05)
    add(sfx, whoosh(), cfg["end"] - 0.25)
    add(sfx, sparkle(0.14), cfg["end"] + 0.1)
    mk = MARKS.get(n, {})
    if n == 2:
        for k in ("banana", "apple", "cat"): add(sfx, pop(), mk[k])
        for k in ("three", "two", "one"): add(sfx, pluck(1046.5, 0.3, 0.14), mk[k])
        add(sfx, ding(), mk["reveal"]); add(sfx, sparkle(0.16), mk["reveal"] + 0.1)
    if n == 3:
        add(sfx, sparkle(0.12), 9.0 + 3.0)
        add(sfx, ding(0.16), MARKS[3]["turn"])
    # duck music under voices
    mus = music(total)
    venv = np.abs(voice).max(axis=1)
    k = int(0.08 * SR)
    sm = np.convolve(venv, np.ones(k) / k, mode="same")
    duck = 1 - 0.62 * np.clip(sm / 0.04, 0, 1)
    mus *= duck[:, None]
    mix = mus * 0.85 + voice + sfx
    mix /= max(1.0, np.abs(mix).max() / 0.95)
    pcm = (mix * 32767).astype(np.int16)
    import wave
    with wave.open(D + f"mix-{n}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
    json.dump(dict(title=cfg["title"], total=total, end=cfg["end"], clips=clips, marks=mk), open(D + f"tl-{n}.json", "w"))
    print(n, "ok", total)


if __name__ == "__main__":
    for n in map(int, sys.argv[1:] or ["1", "2", "3"]):
        build(n)
