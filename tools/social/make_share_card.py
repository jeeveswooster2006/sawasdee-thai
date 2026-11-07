"""Link-preview picture (1200x630) with all four mascots: art/share/nongchang-share-4.png"""
from PIL import Image, ImageDraw, ImageFont
import sys
F = sys.argv[1] if len(sys.argv) > 1 else "fonts/"
W, H = 1200, 630
BG, DARK, TEAL, GOLD = (238, 245, 240), (22, 52, 46), (14, 122, 104), (226, 154, 40)
share = Image.open("art/share/nongchang-share.png").convert("RGB")
img = Image.new("RGB", (W, H), BG)
# Keep the dotted edges of the old card.
img.paste(share.crop((0, 0, W, 22)), (0, 0)); img.paste(share.crop((0, H - 22, W, H)), (0, H - 22))
d = ImageDraw.Draw(img)
f = lambda n, s: ImageFont.truetype(F + n, s, layout_engine=ImageFont.Layout.RAQM)
def centre(text, font, y, fill):
    w = d.textlength(text, font=font); d.text(((W - w) / 2, y), text, font=font, fill=fill)
centre("Nong Chang & Family", f("Mitr-SemiBold.ttf", 66), 40, DARK)
centre("Learn a language together – grown-ups & kids", f("Mitr-Medium.ttf", 34), 130, TEAL)
# Mascots: (file, crop box)
M = [("art/share/nongchang-share.png", (700, 95, 1148, 543), "Thai"),
     ("courses/es/art/mascot.png", (25, 30, 385, 390), "Spanish"),
     ("courses/fr/art/mascot.png", (300, 120, 920, 740), "French"),
     ("courses/it/art/mascot.png", (230, 60, 870, 700), "Italian")]
D, gap = 236, 40
x0 = (W - (4 * D + 3 * gap)) // 2
lab = f("Mitr-SemiBold.ttf", 34)
for i, (p, box, name) in enumerate(M):
    src = Image.open(p).convert("RGB").crop(box).resize((D, D), Image.LANCZOS)
    mask = Image.new("L", (D, D), 0); ImageDraw.Draw(mask).ellipse((0, 0, D - 1, D - 1), fill=255)
    x, y = x0 + i * (D + gap), 205
    d.ellipse((x - 7, y - 7, x + D + 7, y + D + 7), fill=(250, 236, 200))
    img.paste(src, (x, y), mask)
    w = d.textlength(name, font=lab); d.text((x + (D - w) / 2, y + D + 22), name, font=lab, fill=DARK)
centre("Free · no ads · nongchang.co.uk", f("Mitr-Medium.ttf", 30), 555, GOLD)
img.save("art/share/nongchang-share-4.png", optimize=True)
