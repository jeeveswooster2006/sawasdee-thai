"""Feature-spotlight and all-language cards (1080x1350) in the app's brand colours, with all five mascots."""
from PIL import Image, ImageDraw, ImageFont

S = "/tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/"
F = S + "fonts/"
OUT = S + "spot/"
W, H = 1080, 1350
MINT, INK, TEAL, GOLD, PINK, SAGE, CREAM, RING, SOFT = "#EEF5F0", "#123B37", "#007767", "#F2A024", "#E0507A", "#4F6B66", "#F6EFE0", "#F3E2B0", "#D3EFE7"
mitr = lambda n: ImageFont.truetype(F + "Mitr-SemiBold.ttf", n)
mitrM = lambda n: ImageFont.truetype(F + "Mitr-Medium.ttf", n)
sara = lambda n: ImageFont.truetype(F + "Sarabun-SemiBold.ttf", n)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines


def centered(d, y, lines, font, fill, gap=1.22):
    for ln in lines:
        d.text((W / 2, y), ln, font=font, fill=fill, anchor="ma")
        y += int(font.size * gap)
    return y


def trim(d, y):
    cols = [TEAL, PINK, GOLD]
    for i, x in enumerate(range(30, W, 44)):
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=cols[i % 3])


def mascots(img, y_base, big=500, small=350):
    order = ["fr", "es", "th", "it", "en"]
    ims = []
    for k in order:
        m = Image.open(S + f"loy/cut/{k}.png").convert("RGBA")
        h = big if k == "th" else small
        m = m.resize((int(m.width * h / m.height), h), Image.LANCZOS)
        if k == "es": m = m.transpose(Image.FLIP_LEFT_RIGHT)  # face the middle
        ims.append(m)
    total = sum(m.width for m in ims) - 110 * (len(ims) - 1)
    scale = min(1.0, (W - 60) / total)
    if scale < 1: ims = [m.resize((int(m.width * scale), int(m.height * scale)), Image.LANCZOS) for m in ims]
    total = sum(m.width for m in ims) - int(110 * scale) * (len(ims) - 1)
    d = ImageDraw.Draw(img)
    d.ellipse((60, y_base - 40, W - 60, y_base + 40), fill=SOFT)
    x = (W - total) // 2
    # draw the outer ones first so Nong Chang overlaps in front
    pos = []
    for m in ims: pos.append(x); x += m.width - int(110 * scale)
    for i in [0, 4, 1, 3, 2]:
        img.alpha_composite(ims[i], (pos[i], y_base - ims[i].height + 10))


def footer(d):
    pill_w = d.textlength("nongchang.co.uk", font=mitr(54)) + 90
    d.rounded_rectangle(((W - pill_w) / 2, 1148, (W + pill_w) / 2, 1236), radius=44, fill=TEAL)
    d.text((W / 2, 1192), "nongchang.co.uk", font=mitr(54), fill="white", anchor="mm")
    d.text((W / 2, 1268), "Free · no ads · works on any phone", font=sara(32), fill=SAGE, anchor="mm")


def tag(d, text, y=105, fill=GOLD, color=INK):
    f = mitrM(34); w = d.textlength(text, font=f) + 60
    d.rounded_rectangle(((W - w) / 2, y, (W + w) / 2, y + 60), radius=30, fill=fill)
    d.text((W / 2, y + 30), text, font=f, fill=color, anchor="mm")


def spotlight(name, title, body):
    img = Image.new("RGBA", (W, H), MINT); d = ImageDraw.Draw(img)
    trim(d, 40); trim(d, H - 40)
    tag(d, "Feature spotlight")
    y = centered(d, 235, wrap(d, title, mitr(86), W - 140), mitr(86), INK, 1.15)
    y = centered(d, y + 24, wrap(d, body, sara(42), W - 170), sara(42), SAGE, 1.3)
    mascots(img, 1105)
    footer(d)
    img.convert("RGB").save(OUT + name + ".png", optimize=True)


def please_card():
    img = Image.new("RGBA", (W, H), MINT); d = ImageDraw.Draw(img)
    trim(d, 40); trim(d, H - 40)
    tag(d, "5 languages")
    centered(d, 200, ["How do you say", "“please”?"], mitr(84), INK, 1.12)
    rows = [("th", "Thai", "กรุณา", "gà-rú-naa (formal, on signs)"), ("fr", "French", "s'il vous plaît", "seel voo PLEH"),
            ("es", "Spanish", "por favor", "por fah-VOR"), ("it", "Italian", "per favore", "pehr fah-VOH-reh"), ("en", "English", "please", "")]
    y = 405
    for k, lang, word, say in rows:
        d.rounded_rectangle((70, y, W - 70, y + 128), radius=36, fill="white", outline=RING, width=4)
        av = Image.open(S + f"loy/av-{k}.png").convert("RGBA").resize((108, 108), Image.LANCZOS)
        img.alpha_composite(av, (86, y + 10))
        d.text((222, y + 20), lang, font=mitrM(30), fill=TEAL)
        d.text((222, y + 54), word, font=sara(48) if k != "th" else sara(46), fill=INK)
        if say: d.text((W - 96, y + 64), say, font=sara(30), fill=SAGE, anchor="rm")
        y += 134
    d.text((W / 2, 1126), "Everyday Thai: ขอ … หน่อย + ครับ/ค่ะ", font=sara(36), fill=INK, anchor="mm")
    pill_w = d.textlength("nongchang.co.uk", font=mitr(50)) + 80
    d.rounded_rectangle(((W - pill_w) / 2, 1168, (W + pill_w) / 2, 1246), radius=40, fill=TEAL)
    d.text((W / 2, 1207), "nongchang.co.uk", font=mitr(50), fill="white", anchor="mm")
    d.text((W / 2, 1276), "Free · no ads · works on any phone", font=sara(30), fill=SAGE, anchor="mm")
    img.convert("RGB").save(OUT + "please-5-languages.png", optimize=True)


spotlight("spotlight-play-together", "Play together", "Two players, one phone. Take turns guessing what each word means, pass the phone, and see who wins!")
spotlight("spotlight-printables", "Printables", "Turn the words your kids know into flashcards or a big “fridge words” sheet. Perfect for a rainy holiday afternoon.")
spotlight("spotlight-family-goal", "The family goal", "Every lesson anyone in the family finishes adds a banana. Fill the pile together by Sunday for a banana party!")
please_card()
print("done")
