"""Long 16:9 compilations from existing Shorts. python3 make_long.py <key>..."""
import json, subprocess, sys, os, re
SP = "/tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/"
Y = "/tmp/claude-0/orig/social/youtube/"
def hol(k): return json.load(open(SP + f"holiday/tl-{k}.json"))["outro"]
def sh(k): return json.load(open(SP + f"shorts/tl-{k}.json"))["end"]
HB = Y + "holiday/batch2/"
LANG = {"fr": "French", "es": "Spanish", "it": "Italian", "th": "Thai"}
FLAG = {"fr": "🇫🇷", "es": "🇪🇸", "it": "🇮🇹", "th": "🇹🇭"}
TOP = {"basics": "First words", "restaurant": "At the restaurant", "shopping": "Shopping", "market": "At the market",
       "directions": "Finding your way", "stuck": "When you're stuck", "emergency": "If something goes wrong", "help": "If something goes wrong"}
def holiday(l):
    tops = ["basics", "restaurant", "market", "directions", "help"] if l == "th" else ["basics", "restaurant", "shopping", "directions", "stuck", "emergency"]
    segs = []
    for t in tops:
        path = Y + f"holiday/holiday-{l}-restaurant.mp4" if t == "restaurant" else HB + f"{l}-{t}.mp4"
        segs.append((path, hol(f"{l}-{t}"), TOP[t]))
    return dict(segs=segs, panel=dict(flag=FLAG[l], h1=f"{LANG[l]}<br><span>for your holiday</span>", sub="Phrases you will really use. Say them out loud in the pause!",
                langs=" · ".join(TOP[t] for t in tops), rt=f"Learn {LANG[l]} in 5 minutes a day, together as a family", friends=False),
                thumb=dict(h1=f"{LANG[l]} for your holiday {FLAG[l]}", h2="Phrases you'll really use"))
SPEC = {f"holiday-{l}": holiday(l) for l in ("fr", "es", "it", "th")}
SPEC["sayings"] = dict(segs=[
    (HB + "fr-sayings1.mp4", hol("fr-sayings1"), "French sayings, part 1"),
    (Y + "pilots/funny-sayings-fame-da-lupi.mp4", sh("3"), "Italian: avere una fame da lupi (Lupo)"),
    (HB + "es-sayings1.mp4", hol("es-sayings1"), "Spanish sayings, part 1"),
    (Y + "batch2/funny-sayings-cha-pen-tao-nong-chang.mp4", sh("tao"), "Thai: ช้าเป็นเต่า (Nong Chang)"),
    (HB + "it-sayings1.mp4", hol("it-sayings1"), "Italian sayings, part 1"),
    (Y + "batch3/funny-sayings-chair-de-poule-coco.mp4", sh("poule"), "French: avoir la chair de poule (Coco)"),
    (HB + "th-sayings1.mp4", hol("th-sayings1"), "Thai sayings, part 1"),
    (Y + "batch2/funny-sayings-memoria-de-pez-torito.mp4", sh("pez"), "Spanish: tener memoria de pez (Torito)"),
    (HB + "fr-sayings2.mp4", hol("fr-sayings2"), "French sayings, part 2"),
    (Y + "batch3/funny-sayings-piove-a-catinelle-lupo.mp4", sh("catinelle"), "Italian: piove a catinelle (Lupo)"),
    (HB + "es-sayings2.mp4", hol("es-sayings2"), "Spanish sayings, part 2"),
    (HB + "it-sayings2.mp4", hol("it-sayings2"), "Italian sayings, part 2"),
    (HB + "th-sayings2.mp4", None, "Thai sayings, part 2")],
    panel=dict(flag="🤯", h1="Funny sayings<br><span>from around the world</span>", sub="Word for word... and what they really mean",
               langs="Thai · French · Spanish · Italian", rt="Learn a language together as a family", friends=True),
    thumb=dict(h1="Funny sayings 😂", h2="that make no sense in English"))
SPEC["first-words"] = dict(segs=[
    (Y + "pilots/say-it-in-5-thank-you.mp4", sh("1"), "Thank you in 5 languages"),
    (Y + "pilots/guess-the-word-la-manzana.mp4", sh("2"), "Guess the word: la manzana"),
    (Y + "batch2/say-it-in-5-hello-leo.mp4", sh("hello"), "Hello in 5 languages"),
    (Y + "batch2/guess-the-word-le-chat-coco.mp4", sh("chat"), "Guess the word: le chat"),
    (Y + "batch3/say-it-in-5-sorry-leo.mp4", sh("sorry5"), "Sorry in 5 languages"),
    (Y + "batch2/guess-the-word-il-gelato-lupo.mp4", sh("gelato"), "Guess the word: il gelato"),
    (Y + "batch3/guess-the-word-la-nieve-torito.mp4", sh("nieve"), "Guess the word: la nieve"),
    (Y + "batch3/guess-the-word-plaa-nong-chang.mp4", None, "Guess the word: ปลา (plaa)")],
    panel=dict(flag="👋", h1="First words<br><span>in 5 languages</span>", sub="Hello, thank you, sorry... and a guess-the-word quiz!",
               langs="Thai · French · Spanish<br>Italian · English", rt="Learn a language together as a family", friends=True),
    thumb=dict(h1="First words in 5 languages 👋", h2="Hello · thank you · sorry + a quiz"))
SPEC["yummy"] = dict(segs=[
    (Y + "yummy/yummy-thai-nong-chang.mp4", sh("ny"), "Thailand: mango sticky rice (Nong Chang)"),
    (Y + "yummy/yummy-french-coco.mp4", sh("co"), "France: a warm croissant (Coco)"),
    (Y + "yummy/yummy-spanish-torito.mp4", sh("to"), "Spain: churros and chocolate (Torito)"),
    (Y + "yummy/yummy-italian-lupo.mp4", sh("lu"), "Italy: cheesy pizza (Lupo)"),
    (Y + "yummy/yummy-english-leo.mp4", sh("le"), "England: scones and jam (Leo)"),
    (Y + "yummy/yummy-in-5.mp4", None, "Your turn: Yummy in 5 languages")],
    panel=dict(flag="😋", h1="Yummy!<br><span>in 5 languages</span>", sub="How to say \"it's delicious\" around the world",
               langs="Thai · French · Spanish<br>Italian · English", rt="Learn a language together as a family", friends=True),
    thumb=dict(h1="Yummy! in 5 languages 😋", h2="Say \"it's delicious\" around the world"))
SPEC["winter"] = dict(segs=[
    (Y + "occasions/inocentes-torito.mp4", sh("xino"), "28 Dec · Spain: Día de los Inocentes"),
    (Y + "occasions/say-it-in-5-happy-new-year-coco.mp4", sh("newyear5"), "31 Dec · Happy New Year in 5 languages"),
    (Y + "occasions/reyes-magos-torito.mp4", sh("xrey"), "5 Jan · Spain: los Reyes Magos"),
    (Y + "occasions/befana-lupo.mp4", sh("xbef"), "6 Jan · Italy: la Befana"),
    (Y + "occasions/epiphany-galette-coco.mp4", sh("xep"), "6 Jan · France: la galette des rois"),
    (Y + "occasions/thai-childrens-day-nong-chang.mp4", None, "9 Jan · Thailand: Children's Day")],
    panel=dict(flag="🎉", h1="Winter festivals<br><span>around the world</span>", sub="New Year, the Three Kings, la Befana and more",
               langs="Spain · France · Italy · Thailand", rt="Learn a language together as a family", friends=True),
    thumb=dict(h1="Winter festivals 🎉", h2="Spain · France · Italy · Thailand"))

def run(cmd): subprocess.run(cmd, check=True)
def dur(p): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p], capture_output=True, text=True).stdout)
def build(key):
    s = SPEC[key]; d = f"out-{key}"; os.makedirs(d, exist_ok=True)
    run(["node", "shot2.cjs", "panels2.html", "1920", "1080", f"{d}/panels.png", json.dumps(s["panel"])])
    lst = open(f"{d}/list.txt", "w"); chapters = []; t = 0.0; frames = []
    for i, (path, cut, name) in enumerate(s["segs"]):
        cut = cut or dur(path); fo = round(cut - 0.35, 3); o = f"{d}/s{i:02d}.mp4"
        fc = (f"[0:v]trim=0:{cut},setpts=PTS-STARTPTS,fps=30,split[a][b];[a]scale=1920:-2,crop=1920:1080,boxblur=28:2,eq=brightness=0.06:saturation=1.15[bg];"
              f"[b]scale=608:1080[fg];[bg][fg]overlay=(W-w)/2:0[m];[m][1:v]overlay=0:0,fade=t=in:st=0:d=0.3:color=white,fade=t=out:st={fo}:d=0.35:color=white,format=yuv420p[v];"
              f"[0:a]atrim=0:{cut},asetpts=PTS-STARTPTS,aresample=48000,afade=t=in:st=0:d=0.15,afade=t=out:st={fo}:d=0.35[au]")
        run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-i", path, "-i", f"{d}/panels.png", "-filter_complex", fc, "-map", "[v]", "-map", "[au]",
             "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", o])
        lst.write(f"file 's{i:02d}.mp4'\n"); chapters.append(f"{int(t//60)}:{int(t%60):02d} {name}"); t += cut
        frames.append((path, cut * 0.45))
    lst.close()
    run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{d}/list.txt", "-c", "copy", "-movflags", "+faststart", f"{d}/{key}-long.mp4"])
    # thumbnail: five frames spread through the video
    pick = [frames[round(j * (len(frames) - 1) / 4)] for j in range(5)]
    fl = []
    for j, (p, at) in enumerate(pick):
        f = f"{d}/th{j}.jpg"; run(["ffmpeg", "-nostdin", "-loglevel", "error", "-y", "-ss", str(at), "-i", p, "-frames:v", "1", "-q:v", "2", f]); fl.append(f)
    run(["node", "shot2.cjs", "thumb2.html", "1280", "720", f"{d}/thumbnail.png", json.dumps(dict(s["thumb"], frames=fl))])
    json.dump(dict(chapters=chapters, total=round(t, 1)), open(f"{d}/chapters.json", "w"), ensure_ascii=False)
    for f in os.listdir(d):
        if re.fullmatch(r"s\d\d\.mp4", f): os.remove(f"{d}/{f}")
    print(key, round(t, 1), "s", os.path.getsize(f"{d}/{key}-long.mp4") // 1_000_000, "MB")
for k in sys.argv[1:] or SPEC: build(k)
