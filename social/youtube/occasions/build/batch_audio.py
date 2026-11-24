"""Second batch of code-made Shorts: timelines + audio from three templates (say5, guess, saying).
Writes tl-<id>.json and mix-<id>.wav. Timings are worked out from each recording's length."""
import json, sys, wave
import numpy as np
import build_audio as B

SR = B.SR
WORDS = json.load(open(B.D + "words-b2.json"))
dur = lambda n: len(B.load(n)) / SR

def word_at(clip, word):
    for w, t in WORDS[clip]:
        if word.lower() in w.lower().strip(",.?!"): return t
    raise KeyError((clip, word))

CFG = {
  "hello": dict(kind="say5", title="Say it in 5!", host="en",
    intro=("b1", "Hi friends, I'm Leo! How do you say hello? Let's ask my friends!"),
    words=[dict(k="th", lang="Thai", flag="🇹🇭", word="สวัสดี", rom="sa-wàt-dii", font="Sarabun", clip="w-th-hello"),
           dict(k="fr", lang="French", flag="🇫🇷", word="Bonjour", clip="w-fr-hello"),
           dict(k="es", lang="Spanish", flag="🇪🇸", word="¡Hola!", clip="w-es-hello"),
           dict(k="it", lang="Italian", flag="🇮🇹", word="Buongiorno", clip="w-it-hello"),
           dict(k="en", lang="English", flag="🇬🇧", word="Hello!", clip="w-en-hello")],
    try_=("b2", "Now you try! Say hello in your favourite language!"),
    end=("le3", "Learn with us at nongchang.co.uk")),
  "rain": dict(kind="say5", title="Say it in 5!", host="th",
    intro=("rn1", "How do you say \"it's raining\" in five languages? Let's ask my friends!"),
    words=[dict(k="th", lang="Thai", flag="🇹🇭", word="ฝนตก", rom="fǒn-tòk", font="Sarabun", clip="w-th-rain"),
           dict(k="fr", lang="French", flag="🇫🇷", word="Il pleut", clip="w-fr-rain"),
           dict(k="es", lang="Spanish", flag="🇪🇸", word="¡Llueve!", clip="w-es-rain"),
           dict(k="it", lang="Italian", flag="🇮🇹", word="Piove", clip="w-it-rain"),
           dict(k="en", lang="English", flag="🇬🇧", word="It's raining!", clip="w-en-rain")],
    try_=("rn2", "Now you try! Say it in your favourite language!"),
    end=("nc3", "Learn with us at nongchang.co.uk")),
  "chat": dict(kind="guess", title="Guess the word!", host="fr", lang="🇫🇷 French",
    intro=("c1", "Can you guess what this word means? Listen!"), word="le chat", wclip="w-chat",
    q=("c2", "Is it a dog... a cat... or a fish?"), choices=[["🐶", "dog"], ["🐱", "cat"], ["🐟", "fish"]], answer=1,
    ans=("c3", "It's a cat! Meow! You're amazing!"), end=("co3", "Learn with us at nongchang.co.uk")),
  "gelato": dict(kind="guess", title="Guess the word!", host="it", lang="🇮🇹 Italian",
    intro=("p1", "Can you guess what this word means? Listen!"), word="il gelato", wclip="w-gelato",
    q=("p2", "Is it a pizza... an ice cream... or a banana?"), choices=[["🍕", "pizza"], ["🍦", "ice cream"], ["🍌", "banana"]], answer=1,
    ans=("p3", "It's an ice cream! Yum! You're amazing!"), end=("lw3", "Learn with us at nongchang.co.uk")),
  "tao": dict(kind="saying", title="Funny sayings!", host="th", lang="🇹🇭 Thai",
    intro=("n1", "Hi, I'm Nong Chang! When Thai people are super, super slow, they say..."),
    phrase=[["ช้า", "cháa"], ["เป็น", "pen"], ["เต่า", "tào"]], pclip="w-tao", thai=True,
    lit=("n2", "That means... slow like a turtle! Slooow... like this!"), literal="“slow like a turtle!”", emo="🐢",
    fall=["🐢", "🐢", "🐌", "🐢", "🐢", "🐌"],
    say=("n3", "Now say it with me!"), end=("nc3", "Learn with us at nongchang.co.uk")),
  "pez": dict(kind="saying", title="Funny sayings!", host="es", lang="🇪🇸 Spanish",
    intro=("r1", "¡Hola! I'm Torito! When someone forgets everything, in Spain we say..."),
    phrase=[["tener", ""], ["memoria", ""], ["de", ""], ["pez", ""]], pclip="w-pez",
    lit=("r2", "That means... to have the memory of a fish! Wait... what was I saying?"), literal="“the memory of a fish!”", emo="🐟",
    fall=["🐟", "❓", "🐠", "🐟", "❓", "🐡"],
    say=("r3", "Now say it with me!"), end=("ty3", "Learn with us at nongchang.co.uk")),
  "xmas5": dict(kind="say5", title="Say it in 5!", host="es",
    intro=("xt1", "¡Hola, friends! How do you say Merry Christmas? Let's ask my friends!"),
    words=[dict(k="th", lang="Thai", flag="🇹🇭", word="สุขสันต์วันคริสต์มาส", rom="sùk-sǎn wan khrít-sà-mâat", font="Sarabun", clip="w-th-xmas"),
           dict(k="fr", lang="French", flag="🇫🇷", word="Joyeux Noël !", clip="w-fr-xmas"),
           dict(k="es", lang="Spanish", flag="🇪🇸", word="¡Feliz Navidad!", clip="w-es-xmas"),
           dict(k="it", lang="Italian", flag="🇮🇹", word="Buon Natale!", clip="w-it-xmas"),
           dict(k="en", lang="English", flag="🇬🇧", word="Merry Christmas!", clip="w-en-xmas")],
    try_=("xt2", "Now you try! Say Merry Christmas in your favourite language!"),
    end=("ty3", "Learn with us at nongchang.co.uk")),
  "gift5": dict(kind="say5", title="Say it in 5!", host="en",
    intro=("xl1", "Hi friends! How do you say \"a present for you\"? Let's ask my friends!"),
    words=[dict(k="th", lang="Thai", flag="🇹🇭", word="ของขวัญให้คุณ", rom="khǒng-khwǎn hâi khun", font="Sarabun", clip="w-th-gift"),
           dict(k="fr", lang="French", flag="🇫🇷", word="Un cadeau pour toi !", clip="w-fr-gift"),
           dict(k="es", lang="Spanish", flag="🇪🇸", word="¡Un regalo para ti!", clip="w-es-gift"),
           dict(k="it", lang="Italian", flag="🇮🇹", word="Un regalo per te!", clip="w-it-gift"),
           dict(k="en", lang="English", flag="🇬🇧", word="A present for you!", clip="w-en-gift")],
    try_=("xl2", "Now you try! Say it in your favourite language!"),
    end=("le3", "Learn with us at nongchang.co.uk")),
  "newyear5": dict(kind="say5", title="Say it in 5!", host="fr",
    intro=("nyc1", "Bonjour, friends! How do you say Happy New Year? Let's ask my friends!"),
    words=[dict(k="th", lang="Thai", flag="🇹🇭", word="สวัสดีปีใหม่", rom="sà-wàt-dii bpii mài", font="Sarabun", clip="w-th-ny"),
           dict(k="fr", lang="French", flag="🇫🇷", word="Bonne année !", clip="w-fr-ny"),
           dict(k="es", lang="Spanish", flag="🇪🇸", word="¡Feliz Año Nuevo!", clip="w-es-ny"),
           dict(k="it", lang="Italian", flag="🇮🇹", word="Buon anno!", clip="w-it-ny"),
           dict(k="en", lang="English", flag="🇬🇧", word="Happy New Year!", clip="w-en-ny")],
    try_=("co2", "Now you try! Say it with me!"),
    end=("co3", "Learn with us at nongchang.co.uk")),
  "sapin": dict(kind="guess", title="Guess the word!", host="fr", lang="🇫🇷 French",
    intro=("c1", "Can you guess what this word means? Listen!"), word="le sapin", wclip="w-sapin",
    q=("xc2", "Is it a snowman... a Christmas tree... or a present?"), choices=[["⛄", "snowman"], ["🎄", "Christmas tree"], ["🎁", "present"]], answer=1,
    ans=("xc3", "It's a Christmas tree! So sparkly! You're amazing!"), end=("co3", "Learn with us at nongchang.co.uk")),
  "regalo": dict(kind="guess", title="Guess the word!", host="it", lang="🇮🇹 Italian",
    intro=("p1", "Can you guess what this word means? Listen!"), word="un regalo per te", wclip="w-regalo",
    q=("xp2", "Is it good night... a present for you... or happy birthday?"), choices=[["🌙", "good night"], ["🎁", "a present for you"], ["🎂", "happy birthday"]], answer=1,
    ans=("xp3", "It's a present for you! Grazie! You're amazing!"), end=("lw3", "Learn with us at nongchang.co.uk")),
}


def build(sid):
    c = CFG[sid]; host = c["host"]; clips = []; marks = {}
    def put(name, at, text=None):
        clips.append(dict(name=name, start=round(at, 3), dur=round(dur(name), 3), who=host, text=text))
        return at + dur(name)
    if c["kind"] == "say5":
        e = put(c["intro"][0], 0.5, c["intro"][1])
        t = e + 0.45
        for i, w in enumerate(c["words"]):
            clips.append(dict(name=w["clip"], start=round(t, 3), dur=round(dur(w["clip"]), 3), who=w["k"], text=None, word=True)); t += 2.0
        e = put(c["try_"][0], t + 0.2, c["try_"][1])
        end = e + 0.7
    elif c["kind"] == "guess":
        e = put(c["intro"][0], 0.5, c["intro"][1])
        w1 = e + 0.35; clips.append(dict(name=c["wclip"], start=round(w1, 3), dur=round(dur(c["wclip"]), 3), who=host, text=None, word=True))
        w2 = w1 + dur(c["wclip"]) + 0.5; clips.append(dict(name=c["wclip"], start=round(w2, 3), dur=round(dur(c["wclip"]), 3), who=host, text=None, word=True))
        q = w2 + dur(c["wclip"]) + 0.6; qe = put(c["q"][0], q, c["q"][1])
        names = [n for _, n in c["choices"]]
        marks["choice"] = [round(q + word_at(c["q"][0], n.split()[-1]) - 0.05, 3) for n in names]
        marks["count"] = [round(qe + 0.05, 3), round(qe + 0.85, 3), round(qe + 1.85, 3)]
        marks["reveal"] = round(qe + 2.65, 3)
        ae = put(c["ans"][0], qe + 2.8, c["ans"][1])
        w3 = ae + 0.3; clips.append(dict(name=c["wclip"], start=round(w3, 3), dur=round(dur(c["wclip"]), 3), who=host, text=None, word=True))
        marks["eq"] = round(w3 - 0.15, 3); marks["w1"] = round(w1, 3); marks["q"] = round(q, 3)
        end = w3 + dur(c["wclip"]) + 1.2
    else:
        e = put(c["intro"][0], 0.5, c["intro"][1])
        p1 = e + 0.4; pd = dur(c["pclip"])
        clips.append(dict(name=c["pclip"], start=round(p1, 3), dur=round(pd, 3), who=host, text=None, word=True))
        if c.get("thai"):
            n = len(c["phrase"]); marks["words"] = [round(i * pd * 0.8 / n, 3) for i in range(n)]
        else:
            ws = WORDS[c["pclip"]]; marks["words"] = [round(t, 3) for _, t in ws][: len(c["phrase"])]
        lit = p1 + pd + 0.6; le = put(c["lit"][0], lit, c["lit"][1])
        marks["lit"] = round(lit, 3); marks["litEnd"] = round(le, 3)
        s = le + 0.4; se = put(c["say"][0], s, c["say"][1])
        p2 = se + 0.3; clips.append(dict(name=c["pclip"], start=round(p2, 3), dur=round(pd, 3), who=host, text=None, word=True))
        marks["turn"] = round(p2 + pd + 0.5, 3)
        end = marks["turn"] + 2.6
    end = round(end, 3)
    put(c["end"][0], end + 0.4, c["end"][1])
    total = round(end + 4.8, 2)
    # ---- audio ----
    N = int(SR * total); voice = np.zeros((N, 2)); sfx = np.zeros((N, 2))
    for cl in clips:
        sig = B.load(cl["name"]); B.add(voice, sig, cl["start"], gain=1.3 if cl.get("word") else 1.0)
        cl["env"] = B.envelope(sig)
        if cl.get("word"): B.add(sfx, B.pop(0.22), cl["start"] - 0.12)
    B.add(sfx, B.sparkle(), 0.05); B.add(sfx, B.whoosh(), end - 0.25); B.add(sfx, B.sparkle(0.14), end + 0.1)
    if c["kind"] == "guess":
        for t in marks["choice"]: B.add(sfx, B.pop(), t)
        for t in marks["count"]: B.add(sfx, B.pluck(1046.5, 0.3, 0.14), t)
        B.add(sfx, B.ding(), marks["reveal"]); B.add(sfx, B.sparkle(0.16), marks["reveal"] + 0.1)
    if c["kind"] == "saying":
        B.add(sfx, B.sparkle(0.12), marks["lit"] + 3.0); B.add(sfx, B.ding(0.16), marks["turn"])
    if c["kind"] == "say5":
        B.add(sfx, B.ding(0.14), [cl for cl in clips if cl.get("word")][-1]["start"] + 1.4)
    mus = B.music(total)
    venv = np.abs(voice).max(axis=1); k = int(0.08 * SR)
    sm = np.convolve(venv, np.ones(k) / k, mode="same")
    mus *= (1 - 0.62 * np.clip(sm / 0.04, 0, 1))[:, None]
    mix = mus * 0.85 + voice + sfx
    mix /= max(1.0, np.abs(mix).max() / 0.95)
    with wave.open(B.D + f"mix-{sid}.wav", "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((mix * 32767).astype(np.int16).tobytes())
    cfg = {k2: v for k2, v in c.items() if k2 not in ("intro", "try_", "q", "ans", "end", "lit", "say")}
    json.dump(dict(id=sid, title=c["title"], total=total, end=end, clips=clips, marks=marks, cfg=cfg), open(B.D + f"tl-{sid}.json", "w"), ensure_ascii=False)
    print(sid, "total", total, "end", end, marks)


if __name__ == "__main__":
    for sid in sys.argv[1:] or list(CFG):
        build(sid)
