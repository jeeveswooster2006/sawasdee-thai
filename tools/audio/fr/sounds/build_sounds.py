"""Build courses/fr/sounds-of-french.json (the French alphabet and pronunciation track) and its audio batches.

Run from the repo root: python3 tools/audio/fr/sounds/build_sounds.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
CUR = json.loads((ROOT / "courses/fr/curriculum.json").read_text(encoding="utf-8"))
WORDS = {w["id"]: w for lv in CUR for u in lv["units"] for l in u["lessons"] for w in l["words"]}

PURE = "French vowels are short and pure: keep your mouth still so they never slide into another sound."


def vowel(slug, letter, roman, word, meaning, emoji, say_letter=None, note=PURE):
    return {"id": f"fr-sp-vowel-{slug}", "kind": "letter", "text": f"{letter.upper()} {letter}",
            "roman": roman, "en": f"{roman}, as in {word} ({meaning})", "emoji": emoji,
            "say": f"{say_letter or letter}, {word}", "note": note}


def abc(letter, name, roman, word, meaning, emoji, note=None):
    return {"id": f"fr-sp-abc-{letter.lower()}", "kind": "letter", "text": f"{letter} {letter.lower()}", "name": name,
            "roman": roman, "en": f"“{name}”, as in {word} ({meaning})", "emoji": emoji,
            "say": f"{name}, {word}",
            "note": note or f"The letter is called “{name}” ({roman}). {word[0].upper() + word[1:]} means {meaning}."}


def sound(slug, text, roman, en, emoji, say, note):
    return {"id": f"fr-sp-sound-{slug}", "kind": "sound", "text": text, "roman": roman, "en": en,
            "emoji": emoji, "say": say, "note": note}


def word(slug, text, roman, en, emoji, note, kind="word", say=None):
    return {"id": f"fr-sp-{kind}-{slug}", "kind": kind, "text": text, "roman": roman, "en": en,
            "emoji": emoji, "say": say or text, "note": note}


def reading(ids):
    out = []
    for i in ids:
        w = WORDS[i]
        out.append({"id": f"fr-sp-read-{i}", "kind": "reading", "audioId": i, "text": w["text"], "en": w["en"],
                    "emoji": w.get("emoji"), **({"accept": w["accept"]} if w.get("accept") else {})})
    return out


def lesson(lid, title, words):
    return {"id": f"fr-sp-{lid}", "title": title, "words": words}


ACCENT_E = "The accent changes the sound of e, not the stress. "
units = [
    {"id": "fr-sp-vowels", "title": "The vowels", "tagline": "Six vowel letters and three accented e's.", "lessons": [
        lesson("vowels-1", "A, E, I, O, U, Y", [
            vowel("a", "a", "ah", "ananas", "pineapple", "🍍"),
            vowel("e", "e", "uh", "menu", "menu", "📋", say_letter="euh",
                  note="The letter e is called “euh” (like the uh in about, with rounded lips). " + PURE),
            vowel("i", "i", "ee", "île", "island", "🏝️"),
            vowel("o", "o", "oh", "orange", "orange", "🍊"),
            vowel("u", "u", "ew", "usine", "factory", "🏭",
                  note="For u, say ee but round your lips as if blowing a candle. It is a sound English does not have."),
            vowel("y", "y", "ee-GREK", "yoyo", "yo-yo", "🪀", say_letter="i grec",
                  note="Y is called “i grec” (ee-GREK), which means Greek i. Yoyo starts with a y like in yes."),
        ]),
        lesson("vowels-2", "É, È, Ê", [
            vowel("e-acute", "é", "ay", "été", "summer", "☀️", note="É has an accent going up. It sounds like ay in day, without the slide."),
            vowel("e-grave", "è", "eh", "zèbre", "zebra", "🦓", note="È has an accent going down. It sounds like the e in bed."),
            vowel("e-circ", "ê", "eh", "forêt", "forest", "🌲", note="Ê has a little hat. It sounds just like è, the e in bed."),
        ]),
    ]},
    {"id": "fr-sp-abc", "title": "The alphabet", "tagline": "The other 20 letters and their French names.", "lessons": [
        lesson("abc-1", "B, C, D, F, G", [
            abc("B", "bé", "bay", "bateau", "boat", "⛵"),
            abc("C", "cé", "say", "cerise", "cherry", "🍒",
                "The letter is called “cé” (say). Before e or i, c sounds like s, as in cerise. Before a, o or u it sounds like k."),
            abc("D", "dé", "day", "dauphin", "dolphin", "🐬"),
            abc("F", "effe", "EF", "fleur", "flower", "🌸"),
            abc("G", "gé", "zhay", "gâteau", "cake", "🍰",
                "The letter is called “gé” (zhay, like the s in measure). Before a, o or u, g is hard like go, as in gâteau."),
        ]),
        lesson("abc-2", "H, J, K, L, M", [
            abc("H", "hache", "ASH", "hibou", "owl", "🦉",
                "The letter is called “hache” (ash), but h is silent in French: hibou sounds like ee-BOO."),
            abc("J", "ji", "zhee", "jupe", "skirt", "👗",
                "The letter is called “ji” (zhee). J sounds like the s in measure: ZHOOP."),
            abc("K", "ka", "kah", "koala", "koala", "🐨",
                "K is rare in French. It only shows up in borrowed words like koala."),
            abc("L", "elle", "EL", "lune", "moon", "🌙"),
            abc("M", "emme", "EM", "maison", "house", "🏠"),
        ]),
        lesson("abc-3", "N, P, Q, R, S", [
            abc("N", "enne", "EN", "nuage", "cloud", "☁️"),
            abc("P", "pé", "pay", "pomme", "apple", "🍎"),
            abc("Q", "ku", "kew", "coq", "rooster", "🐓",
                "The letter is called “ku” (kew, with the French u sound). At the end of a word, as in coq, q sounds like k."),
            abc("R", "erre", "AIR", "robot", "robot", "🤖",
                "The letter is called “erre” (air). The French r comes from the back of your throat."),
            abc("S", "esse", "ESS", "salade", "salad", "🥗"),
        ]),
        lesson("abc-4", "T, V, W, X, Z", [
            abc("T", "té", "tay", "tortue", "tortoise", "🐢"),
            abc("V", "vé", "vay", "vache", "cow", "🐄"),
            abc("W", "double vé", "DOO-bluh-VAY", "wagon", "train carriage", "🚃",
                "“Double vé” means double v. W only appears in borrowed words like wagon, which French says with a v: vah-GON."),
            abc("X", "iks", "eeks", "taxi", "taxi", "🚕",
                "The letter is called “iks” (eeks). In taxi, x sounds like ks."),
            abc("Z", "zède", "ZED", "zoo", "zoo", "🦁",
                "The letter is called “zède” (zed). Zoo is said ZOH, with a long oh."),
        ]),
    ]},
    {"id": "fr-sp-tricky", "title": "Tricky sounds", "tagline": "The sounds English speakers mix up.", "lessons": [
        lesson("tricky-1", "U, OU, EU and OI", [
            sound("u", "u", "ew", "ew (lips round), as in tu (you)", "🫵", "tu",
                  "Say ee, then round your lips: tew. It is not the same as ou!"),
            sound("ou", "ou", "oo", "oo, as in tout (everything)", "💯", "tout",
                  "Like oo in food: TOO. Tu (you) and tout (everything) only differ by the lips."),
            sound("eu", "eu", "uh", "uh (lips round), as in bleu (blue)", "🔵", "bleu",
                  "Say ay as in day, but with your lips rounded as if for oo: BLUH."),
            sound("oi", "oi", "wah", "wah, as in roi (king)", "👑", "roi",
                  "Oi always sounds like wah: RWAH."),
        ]),
        lesson("tricky-2", "The R and nasal sounds", [
            sound("r", "r", "throaty r", "a throaty r, as in radio (radio)", "📻", "radio",
                  "Make a soft gargle at the back of your throat, like gently clearing it. Do not roll your tongue: rah-dyoh."),
            sound("an", "an · en", "ahn (nasal)", "ahn, as in enfant (child)", "🧒", "enfant",
                  "Nasal means some air goes through your nose. Say ah, then let it hum: ahn-FAHN, without a hard n."),
            sound("on", "on", "ohn (nasal)", "ohn, as in ballon (balloon)", "🎈", "ballon",
                  "Say oh with rounded lips and let it hum in your nose: bah-LOHN, with no hard n."),
            sound("in", "in · un", "an (nasal)", "an, as in lapin (rabbit)", "🐰", "lapin",
                  "Like the a in cat, but through your nose: lah-PAN. Un (one) sounds almost the same."),
        ]),
        lesson("tricky-3", "CH, GN, QU and silent letters", [
            sound("ch", "ch", "sh", "sh, as in chat (cat)", "🐱", "chat", "Not like English church! French ch sounds like sh: SHAH."),
            sound("gn", "gn", "ny", "ny, as in agneau (lamb)", "🐑", "agneau", "Like the ny in canyon: ah-NYOH."),
            sound("qu", "qu", "k", "k, as in raquette (racket)", "🎾", "raquette", "The u after q is silent: qu sounds like k, rah-KET."),
            sound("h", "h", "silent", "silent, as in hôtel (hotel)", "🏨", "hôtel", "H is never pronounced: oh-TEL."),
            sound("final-t", "-t", "silent t", "silent t, as in petit (small)", "🤏", "petit",
                  "Final letters are often silent. The t in petit is not said: puh-TEE."),
            sound("final-d", "-d", "silent d", "silent d, as in grand (big)", "🐘", "grand",
                  "The d in grand is silent, and an makes a nasal sound: GRAHN, with no hard n."),
        ]),
    ]},
    {"id": "fr-sp-accents", "title": "Accents and marks", "tagline": "Little marks that change the sound or meaning.", "lessons": [
        lesson("accents-1", "Accents on E", [
            word("bebe", "bébé", "bay-BAY", "baby (é sounds like ay)", "👶", ACCENT_E + "É is ay, as in day: bay-BAY."),
            word("creme", "crème", "KREM", "cream (è sounds like eh)", "🍦", ACCENT_E + "È is eh, as in bed: KREM."),
            word("fete", "fête", "FET", "party (ê sounds like eh)", "🎉", ACCENT_E + "Ê sounds like è; the hat often shows a lost s from old French."),
        ]),
        lesson("accents-2", "Other marks", [
            word("a-grave", "voilà", "vwah-LAH", "there you go (à)", "👉",
                 "The accent on à does not change the sound. It mostly tells apart a (has) and à (to or at).", kind="mark"),
            word("cedilla", "garçon", "gar-SOHN", "boy (ç sounds like s)", "👦",
                 "The little tail on ç makes it sound like s, even before a, o or u. Without it, c would sound like k.", kind="mark"),
            word("noel", "Noël", "no-EL", "Christmas (ë: say both vowels)", "🎄",
                 "The two dots (tréma) tell you to say the vowel separately: no-EL, not nowl.", kind="mark"),
            word("mais", "maïs", "mah-EESS", "sweetcorn (ï: say both vowels)", "🌽",
                 "The two dots (tréma) on ï keep the a and i apart: mah-EESS.", kind="mark"),
            word("les-amis", "les amis", "lay-zah-MEE", "the friends (liaison)", "🧑‍🤝‍🧑",
                 "Liaison: the silent s of les joins the next vowel and sounds like z. Say lay-zah-MEE.", kind="mark"),
        ]),
    ]},
    {"id": "fr-sp-reading", "title": "Read real words", "tagline": "Use your new sounds on words you know.", "lessons": [
        lesson("reading-1", "Read greetings", reading(["fr-b1-l1-0", "fr-b1-l1-1", "fr-b1-l1-4", "fr-b1-l2-0", "fr-b1-l2-4"])),
        lesson("reading-2", "Read numbers", reading(["fr-n1-l1-0", "fr-n1-l1-1", "fr-n1-l1-2", "fr-n1-l1-3", "fr-n1-l1-4"])),
        lesson("reading-3", "Read family words", reading(["fr-fam-l1-0", "fr-fam-l1-1", "fr-fam-l1-2", "fr-fam-l1-3", "fr-fam-l2-0"])),
    ]},
]
track = [{"level": "Sounds of French", "units": units}]

# checks: unique ids, unique answers within each lesson, no example word used twice
ids = [w["id"] for u in units for l in u["lessons"] for w in l["words"]]
assert len(ids) == len(set(ids)), "duplicate ids"
for u in units:
    for l in u["lessons"]:
        for key in ("en", "text"):
            vals = [w[key] for w in l["words"]]
            assert len(vals) == len(set(vals)), (l["id"], key)
        says = [w["say"] for w in l["words"] if "say" in w]
        assert len(says) == len(set(says)), (l["id"], "say")
recorded = [w for u in units for l in u["lessons"] for w in l["words"] if "audioId" not in w]
example_words = [w["say"].split(", ")[-1] for w in recorded if w["kind"] == "letter"] + \
                [w["say"] for w in recorded if w["kind"] != "letter"]
assert len(example_words) == len(set(example_words)), "example word reused"
emojis = [w["emoji"] for w in recorded]
dup_emoji = sorted({e for e in emojis if emojis.count(e) > 1})
assert not dup_emoji, ("repeated emoji", dup_emoji)

(ROOT / "courses/fr/sounds-of-french.json").write_text(json.dumps(track, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

# batches: at most 26 items and 300 prompt characters each
PREFIX, SEP, MAX_ITEMS, MAX_CHARS = "[slowly, clearly] ", " ... ", 26, 300
chunks, cur = [], []
for w in recorded:
    trial = cur + [w]
    if cur and (len(trial) > MAX_ITEMS or len(PREFIX + SEP.join(x["say"] for x in trial)) > MAX_CHARS):
        chunks.append(cur)
        cur = [w]
    else:
        cur = trial
chunks.append(cur)
groups = [{"group": g, "ids": [w["id"] for w in chunk], "texts": [w["say"] for w in chunk],
           "prompt": PREFIX + SEP.join(w["say"] for w in chunk)} for g, chunk in enumerate(chunks)]
(pathlib.Path(__file__).parent / "audio_groups.json").write_text(json.dumps(groups, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(ids), "items,", len(recorded), "to record in", len(groups), "batches;",
      sum(len(g["prompt"]) for g in groups), "prompt characters")
