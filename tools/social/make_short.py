"""Make a vertical 'Thai word' short (1080x1920) from the course content.

Usage: python tools/social/make_short.py WORD_ID ART_UNIT OUT.mp4
  e.g. python tools/social/make_short.py b1-l1-1 basics1 thank-you.mp4
Needs Pillow and ffmpeg. Later: swap the still scenes for ComfyUI-animated clips of Nong Chang.
"""
import json, subprocess, sys, tempfile, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SP = os.path.join(HERE, "build")
F = os.path.join(HERE, "fonts") + "/"
FONT_URLS = {n: f"https://raw.githubusercontent.com/google/fonts/main/ofl/{n.split('-')[0].lower()}/{n}"
             for n in ["Mitr-SemiBold.ttf", "Mitr-Medium.ttf", "Sarabun-SemiBold.ttf"]}


def ensure_fonts():
    import urllib.request
    os.makedirs(F, exist_ok=True)
    os.makedirs(SP, exist_ok=True)
    for n, u in FONT_URLS.items():
        if not os.path.exists(F + n):
            urllib.request.urlretrieve(u, F + n)
DEJAVU = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # needs IPA glyphs for the romanisation
W, H = 1080, 1920
BG = (238, 245, 240); DARK = (18, 56, 47); MUTED = (79, 107, 99)
GOLD = (226, 150, 40); TEAL = (15, 127, 111); CREAM = (250, 236, 206)
DOTS = [(224, 86, 122), (240, 180, 60), (15, 127, 111)]


def font(name, size):
    return ImageFont.truetype(name if name.startswith("/") else F + name, size)


def find_word(word_id):
    for lvl in json.load(open(f"{REPO}/data/curriculum.json")):
        for u in lvl["units"]:
            for l in u["lessons"]:
                for w in l["words"]:
                    if w["id"] == word_id:
                        return w
    raise SystemExit(f"word {word_id} not found")


def base():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    for y in (14, H - 14):
        for i, x in enumerate(range(10, W, 22)):
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=DOTS[i % 3])
    return img, d


def centered(d, y, text, f, fill):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)


def fit(d, text, fname, size, maxw):
    while d.textlength(text, font=font(fname, size)) > maxw and size > 20:
        size -= 4
    return font(fname, size)


def mascot(img, art_unit, cy, r):
    src = Image.open(f"{REPO}/art/units/{art_unit}.webp").convert("RGB")
    sw, sh = src.size
    side = min(sw, sh) - 60
    left = (sw - side) // 2
    crop = src.crop((left, 20, left + side, 20 + side)).resize((2 * r, 2 * r), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    cx = W // 2
    d.ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), fill=CREAM)
    m = Image.new("L", (2 * r, 2 * r), 0)
    ImageDraw.Draw(m).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    img.paste(crop, (cx - r, cy - r), m)


def pill(d, y, text, f, fill=TEAL, color=(255, 255, 255)):
    tw = d.textlength(text, font=f)
    x0 = (W - tw) / 2 - 40
    d.rounded_rectangle((x0, y, x0 + tw + 80, y + f.size + 44), radius=(f.size + 44) // 2, fill=fill)
    d.text((x0 + 40, y + 18), text, font=f, fill=color)


def scenes(w, art):
    en = w["en"].rstrip("?!.")
    frames = []
    # 1. Hook
    img, d = base()
    centered(d, 230, "How do you say", font("Mitr-Medium.ttf", 76), MUTED)
    centered(d, 330, f"“{en}”", fit(d, f"“{en}”", "Mitr-SemiBold.ttf", 150, 940), DARK)
    centered(d, 520, "in Thai?", font("Mitr-Medium.ttf", 76), MUTED)
    mascot(img, art, 1060, 330)
    frames.append(img)
    # 2. The word
    img, d = base()
    mascot(img, art, 470, 230)
    centered(d, 770, w["thai"], fit(d, w["thai"], "Mitr-SemiBold.ttf", 220, 960), DARK)
    centered(d, 1080, w["roman"], fit(d, w["roman"], DEJAVU, 84, 960), GOLD)
    centered(d, 1210, f"= {w['en']}", fit(d, f"= {w['en']}", "Mitr-Medium.ttf", 72, 960), MUTED)
    if w.get("tone"):
        pill(d, 1340, f"{w['tone']} tone", font("Sarabun-SemiBold.ttf", 46), fill=(226, 238, 232), color=TEAL)
    frames.append(img)
    # 3. Slowly
    img2 = img.copy(); d2 = ImageDraw.Draw(img2)
    pill(d2, 1340, "now slowly…", font("Sarabun-SemiBold.ttf", 46), fill=GOLD)
    frames.append(img2)
    # 4. Your turn
    img, d = base()
    centered(d, 330, "Your turn!", font("Mitr-SemiBold.ttf", 130), TEAL)
    centered(d, 520, "Say it out loud 3 times", font("Mitr-Medium.ttf", 62), MUTED)
    centered(d, 800, w["thai"], fit(d, w["thai"], "Mitr-SemiBold.ttf", 200, 960), DARK)
    centered(d, 1100, w["roman"], fit(d, w["roman"], DEJAVU, 80, 960), GOLD)
    frames.append(img)
    # 5. End card
    img, d = base()
    mascot(img, art, 620, 280)
    centered(d, 980, "Nong Chang", font("Mitr-SemiBold.ttf", 120), DARK)
    centered(d, 1120, "& Family", font("Mitr-SemiBold.ttf", 90), TEAL)
    centered(d, 1260, "Learn Thai together – free", font("Mitr-Medium.ttf", 58), MUTED)
    pill(d, 1380, "Link in bio", font("Sarabun-SemiBold.ttf", 52))
    frames.append(img)
    return frames


def main(word_id, art, out):
    ensure_fonts()
    w = find_word(word_id)
    audio = f"{REPO}/audio/{w.get('audioId', word_id)}.mp3"
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]))
    # scene lengths (seconds)
    hook, word, slow, turn, end = 2.4, max(2.6, dur + 1.4), max(3.0, dur / 0.7 + 1.2), max(4.0, dur * 3 + 2.4), 3.0
    lens = [hook, word, slow, turn, end]
    tmp = tempfile.mkdtemp(dir=SP)
    for i, im in enumerate(scenes(w, art)):
        im.save(f"{tmp}/s{i}.png")
    with open(f"{tmp}/list.txt", "w") as fh:
        for i, L in enumerate(lens):
            fh.write(f"file 's{i}.png'\nduration {L}\n")
        fh.write(f"file 's{len(lens)-1}.png'\n")
    t_word = hook + 0.5
    t_slow = hook + word + 0.6
    t_turn = hook + word + slow + 0.6  # model once, then pauses for the viewer
    total = sum(lens)
    fc = (
        f"[1:a]adelay={int(t_word*1000)}|{int(t_word*1000)}[a1];"
        f"[2:a]atempo=0.7,adelay={int(t_slow*1000)}|{int(t_slow*1000)}[a2];"
        f"[3:a]adelay={int(t_turn*1000)}|{int(t_turn*1000)}[a3];"
        f"[a1][a2][a3]amix=inputs=3:normalize=0,apad,atrim=0:{total}[a]"
    )
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt",
        "-i", audio, "-i", audio, "-i", audio, "-filter_complex", fc,
        "-map", "0:v", "-map", "[a]", "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-t", f"{total}", "-movflags", "+faststart", out,
    ], check=True)
    print(out, round(total, 1), "s")


if __name__ == "__main__":
    main(*sys.argv[1:4])
