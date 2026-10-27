"""Build courses/es/sounds-of-spanish.json (the Spanish alphabet track) and its audio batches.

Run from the repo root: python3 tools/audio/es/sounds/build_sounds.py
"""
import json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[4]
CUR = json.loads((ROOT / "courses/es/curriculum.json").read_text(encoding="utf-8"))
WORDS = {w["id"]: w for lv in CUR for u in lv["units"] for l in u["lessons"] for w in l["words"]}

PURE = "Spanish vowels are short and pure: they never slide into another sound like English 'oh-oo'."


def vowel(letter, roman, word, meaning, emoji):
    return {"id": f"es-sp-vowel-{letter.lower()}", "kind": "letter", "text": f"{letter} {letter.lower()}",
            "roman": roman, "en": f"{roman}, as in {word} ({meaning})", "emoji": emoji,
            "say": f"{letter.lower()}, {word}", "note": PURE}


def abc(letter, name, roman, word, meaning, emoji, note=None):
    slug = {"Ñ": "nn"}.get(letter, letter.lower())
    return {"id": f"es-sp-abc-{slug}", "kind": "letter", "text": f"{letter} {letter.lower()}", "name": name,
            "roman": roman, "en": f"“{name}”, as in {word} ({meaning})", "emoji": emoji,
            "say": f"{name}, {word}",
            "note": note or f"The letter is called “{name}” ({roman}). {word[0].upper() + word[1:]} means {meaning}."}


def sound(slug, text, roman, en, emoji, say, note):
    return {"id": f"es-sp-sound-{slug}", "kind": "sound", "text": text, "roman": roman, "en": en,
            "emoji": emoji, "say": say, "note": note}


def word(slug, text, roman, en, emoji, note, kind="word", say=None):
    return {"id": f"es-sp-{kind}-{slug}", "kind": kind, "text": text, "roman": roman, "en": en,
            "emoji": emoji, "say": say or text, "note": note}


def reading(ids):
    out = []
    for i in ids:
        w = WORDS[i]
        out.append({"id": f"es-sp-read-{i}", "kind": "reading", "audioId": i, "text": w["text"], "en": w["en"],
                    "emoji": w.get("emoji"), **({"accept": w["accept"]} if w.get("accept") else {})})
    return out


def lesson(lid, title, words):
    return {"id": f"es-sp-{lid}", "title": title, "words": words}


STRESS = "No accent? Words ending in a vowel, n or s stress the second-last syllable; others stress the last. An accent overrides the rule."
units = [
    {"id": "es-sp-vowels", "title": "The five vowels", "tagline": "Short, pure sounds that never change.", "lessons": [
        lesson("vowels-1", "A, E, I, O, U", [
            vowel("A", "ah", "agua", "water", "💧"), vowel("E", "eh", "elefante", "elephant", "🐘"),
            vowel("I", "ee", "isla", "island", "🏝️"), vowel("O", "oh", "oso", "bear", "🐻"),
            vowel("U", "oo", "uva", "grape", "🍇"),
        ])]},
    {"id": "es-sp-abc", "title": "The alphabet", "tagline": "27 letters and their names.", "lessons": [
        lesson("abc-1", "B to H", [
            abc("B", "be", "beh", "barco", "boat", "⛵"), abc("C", "ce", "theh", "casa", "house", "🏠"),
            abc("D", "de", "deh", "dedo", "finger", "☝️"), abc("F", "efe", "EH-feh", "fresa", "strawberry", "🍓"),
            abc("G", "ge", "heh", "gato", "cat", "🐱"),
            abc("H", "hache", "AH-cheh", "helado", "ice cream", "🍦",
                "The letter is called “hache” (AH-cheh), but h is always silent: helado sounds like eh-LAH-doh."),
        ]),
        lesson("abc-2", "J to Ñ", [
            abc("J", "jota", "HOH-tah", "jirafa", "giraffe", "🦒"), abc("K", "ka", "kah", "kiwi", "kiwi", "🥝"),
            abc("L", "ele", "EH-leh", "luna", "moon", "🌙"), abc("M", "eme", "EH-meh", "mano", "hand", "✋"),
            abc("N", "ene", "EH-neh", "nube", "cloud", "☁️"),
            abc("Ñ", "eñe", "EH-nyeh", "niño", "child", "🧒",
                "Ñ is its own letter, called “eñe” (EH-nyeh). It sounds like the ny in canyon."),
        ]),
        lesson("abc-3", "P to T", [
            abc("P", "pe", "peh", "perro", "dog", "🐶"), abc("Q", "cu", "koo", "queso", "cheese", "🧀",
                "The letter is called “cu” (koo). Q is always followed by a silent u: queso sounds like KEH-soh."),
            abc("R", "erre", "EH-rreh", "ratón", "mouse", "🐭",
                "The letter is called “erre”. At the start of a word r is rolled, like rr."),
            abc("S", "ese", "EH-seh", "sol", "sun", "☀️"), abc("T", "te", "teh", "tomate", "tomato", "🍅"),
        ]),
        lesson("abc-4", "V to Z", [
            abc("V", "uve", "OO-beh", "vaca", "cow", "🐄",
                "The letter is called “uve” in Spain. V sounds just like b: vaca sounds like BAH-kah."),
            abc("W", "uve doble", "OO-beh DOH-bleh", "wifi", "Wi-Fi", "📶",
                "“Uve doble” means double v. W only appears in borrowed words like wifi."),
            abc("X", "equis", "EH-kees", "taxi", "taxi", "🚕"),
            abc("Y", "ye", "yeh", "yogur", "yoghurt", "🥛",
                "The letter is called “ye” (yeh); older people may say “i griega”. On its own, y means and."),
            abc("Z", "zeta", "THEH-tah", "zapato", "shoe", "👟",
                "The letter is called “zeta”. In Spain z sounds like th in think: thah-PAH-toh."),
        ]),
    ]},
    {"id": "es-sp-tricky", "title": "Tricky sounds", "tagline": "The sounds English speakers mix up.", "lessons": [
        lesson("tricky-1", "Ñ, LL, R, RR and CH", [
            sound("ny", "ñ", "ny", "ny, as in España (Spain)", "🇪🇸", "España", "Like the ny in canyon: es-PAH-nyah."),
            sound("ll", "ll", "y", "y, as in llave (key)", "🔑", "llave", "In most of Spain ll sounds like the y in yes: YAH-beh."),
            sound("r", "r", "tapped r", "a quick tap, as in pero (but)", "↔️", "pero",
                  "Between vowels, one r is a single quick tap of the tongue, like the tt in American butter."),
            sound("rr", "rr", "rolled r", "a rolled r, as in perro (dog)", "🐶", "perro",
                  "Roll your tongue for rr. Pero (but) and perro (dog) only differ by the roll!"),
            sound("ch", "ch", "ch", "ch, as in chocolate (chocolate)", "🍫", "chocolate", "Just like English ch in church."),
        ]),
        lesson("tricky-2", "C, Z and QU in Spain", [
            sound("ca", "ca · co · cu", "k", "k, as in coche (car)", "🚗", "coche", "Before a, o or u, c is a k sound: KOH-cheh."),
            sound("ce", "ce · ci", "th", "th, as in cinco (five)", "🖐️", "cinco",
                  "In Spain, c before e or i sounds like th in think: THEEN-koh."),
            sound("z", "z", "th", "th, as in zumo (juice)", "🧃", "zumo", "In Spain z also sounds like th in think: THOO-moh."),
            sound("qu", "que · qui", "k", "k, as in queso (cheese)", "🧀", "queso", "The u after q is silent: KEH-soh."),
        ]),
        lesson("tricky-3", "J, G and the silent H", [
            sound("j", "j", "throaty h", "a throaty h, as in jamón (ham)", "🍖", "jamón",
                  "Breathe it from the back of your throat, like ch in Scottish loch: hah-MON."),
            sound("ge", "ge · gi", "throaty h", "a throaty h, as in gente (people)", "👥", "gente",
                  "Before e or i, g sounds like j: HEN-teh."),
            sound("ga", "ga · go · gu", "g", "a hard g, as in gafas (glasses)", "👓", "gafas",
                  "Before a, o or u, g is a hard g, as in go."),
            sound("gue", "gue · gui", "g", "a hard g, as in guitarra (guitar)", "🎸", "guitarra",
                  "The u is silent here, it just keeps the g hard: gee-TAH-rrah."),
            sound("h", "h", "silent", "silent, as in hola (hello)", "👋", "hola", "H is never pronounced: OH-lah."),
        ]),
    ]},
    {"id": "es-sp-accents", "title": "Accents and marks", "tagline": "Little marks that change the sound or meaning.", "lessons": [
        lesson("accents-1", "Where's the stress?", [
            word("casa", "casa", "KAH-sah", "house (stress on CA)", "🏠", STRESS),
            word("cafe", "café", "kah-FEH", "coffee (stress on FÉ)", "☕", "The accent on é moves the stress to the end: kah-FEH."),
            word("arbol", "árbol", "AR-bol", "tree (stress on ÁR)", "🌳", "The accent on á puts the stress on the first syllable."),
            word("musica", "música", "MOO-see-kah", "music (stress on MÚ)", "🎵", "The accent on ú puts the stress on MÚ."),
            word("avion", "avión", "ah-bee-ON", "plane (stress on ÓN)", "✈️", "The accent on ó puts the stress at the end."),
        ], ),
        lesson("accents-2", "Special marks", [
            word("que", "¿Qué?", "keh", "What? (¿ opens a question)", "❓",
                 "Spanish questions start with an upside-down ¿ and end with ?.", kind="mark"),
            word("hola", "¡Hola!", "OH-lah", "Hello! (¡ opens an exclamation)", "🎉",
                 "Exclamations start with an upside-down ¡ and end with !.", kind="mark"),
            word("pinguino", "pingüino", "peen-GWEE-noh", "penguin (ü: say the u)", "🐧",
                 "The two dots on ü mean you do say the u: gwee, not gee.", kind="mark"),
            word("si", "sí", "see", "yes (si without the accent means if)", "✅",
                 "Sí with an accent means yes; si without it means if. They sound the same.", kind="mark"),
            word("tu", "tú", "too", "you (tu without the accent means your)", "🫵",
                 "Tú with an accent means you; tu without it means your. They sound the same.", kind="mark"),
        ]),
    ]},
    {"id": "es-sp-reading", "title": "Read real words", "tagline": "Use your new sounds on words you know.", "lessons": [
        lesson("reading-1", "Read greetings", reading(["es-b1-l1-0", "es-b1-l1-1", "es-b1-l1-4", "es-b1-l2-0", "es-b1-l2-4"])),
        lesson("reading-2", "Read numbers", reading(["es-n1-l1-0", "es-n1-l1-1", "es-n1-l1-2", "es-n1-l1-3", "es-n1-l1-4"])),
        lesson("reading-3", "Read family words", reading(["es-fam-l1-0", "es-fam-l1-1", "es-fam-l1-2", "es-fam-l2-0", "es-fam-l2-1"])),
    ]},
]
track = [{"level": "Sounds of Spanish", "units": units}]

# checks: unique ids, unique answers within each lesson
ids = [w["id"] for u in units for l in u["lessons"] for w in l["words"]]
assert len(ids) == len(set(ids)), "duplicate ids"
for u in units:
    for l in u["lessons"]:
        for key in ("en", "text"):
            vals = [w[key] for w in l["words"]]
            assert len(vals) == len(set(vals)), (l["id"], key)
        if l["id"] != "es-sp-reading-1":
            says = [w.get("say") for w in l["words"] if "say" in w]
            assert len(says) == len(set(says)), (l["id"], "say")

(ROOT / "courses/es/sounds-of-spanish.json").write_text(json.dumps(track, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

recorded = [w for u in units for l in u["lessons"] for w in l["words"] if "audioId" not in w]
half = (len(recorded) + 1) // 2
groups = []
for g, chunk in enumerate([recorded[:half], recorded[half:]]):
    groups.append({"group": g, "ids": [w["id"] for w in chunk], "texts": [w["say"] for w in chunk],
                   "prompt": "[slowly, clearly] " + " ... ".join(w["say"] for w in chunk)})
(pathlib.Path(__file__).parent / "audio_groups.json").write_text(json.dumps(groups, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print(len(ids), "items,", len(recorded), "to record in", len(groups), "batches;",
      sum(len(g["prompt"]) for g in groups), "prompt characters")
