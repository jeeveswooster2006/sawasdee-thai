"""Batch 2 of the grown-up Shorts: holiday phrases by topic, and 'sayings' (idioms word for word)."""
import json
C = "/home/user/sawasdee-thai/"
COUNTRY = {"th": "Thailand", "fr": "France", "es": "Spain", "it": "Italy"}
LANG = {"th": "Thai", "fr": "French", "es": "Spanish", "it": "Italian"}
FLAG = {"th": "🇹🇭", "fr": "🇫🇷", "es": "🇪🇸", "it": "🇮🇹"}

def index():
    out = {}
    def walk(x):
        if isinstance(x, dict):
            if "id" in x and "en" in x and ("thai" in x or "text" in x): out[x["id"]] = x
            for v in x.values(): walk(v)
        elif isinstance(x, list):
            for v in x: walk(v)
    walk(json.load(open(C + "data/curriculum.json")))
    for L in ("fr", "es", "it"): walk(json.load(open(C + f"courses/{L}/curriculum.json")))
    walk(json.load(open(C + "tools/content/fun-sayings.json")))
    return out

def audio(L, i):
    return f"audio/{i}.mp3" if L == "th" else f"courses/{L}/audio/{i}.mp3"

TOPICS = {
    "shopping": ("Shopping in {c}?", "4 {l} phrases for markets and shops", "🛍️", ["shop-l1-0", "shop-l1-3", "shop-l1-1", "shop-l1-5"]),
    "basics": ("Off to {c}?", "The 4 {l} words to learn first", "👋", ["b1-l1-0", "phr-l1-0", "b1-l1-1", "b1-l1-4"]),
    "stuck": ("Lost for words in {c}?", "3 {l} phrases for when you're stuck", "🤔", ["phr-l1-4", "phr-l1-5", "phr-l1-3"]),
    "directions": ("Lost in {c}?", "4 {l} phrases for finding your way", "🧭", ["dir2-l1-0", "dir2-l1-1", "dir2-l1-2", "dir2-l1-5"]),
    "emergency": ("An emergency in {c}?", "4 {l} phrases you hope you'll never need", "🚑", ["emg-l1-0", "emg-l1-2", "emg-l1-3", "emg-l1-5"]),
}
THAI = {
    "market": ("Shopping at a Thai market?", "4 Thai phrases for haggling", "🛍️", ["phr-l1-3", "phr-l1-4", "shop-l1-2", "shop-l1-3"]),
    "basics": ("Off to Thailand?", "The 4 Thai phrases to learn first", "👋", ["b1-l1-0", "b1-l1-1", "b1-l1-4", "dlg-l2-0"]),
    "directions": ("Lost in Thailand?", "4 Thai phrases for finding your way", "🧭", ["phr-l2-0", "dir2-l1-0", "dir2-l1-1", "dir2-l1-2"]),
    "help": ("Need help in Thailand?", "3 Thai words for an emergency", "🚑", ["emg-l1-0", "feel-l2-3", "pl-l1-4"]),
}
SAYINGS = {
    "th": [["fun1-l1-0", "fun1-l1-3", "fun3-l1-1"], ["fun3-l1-0", "fun2-l1-1", "fun3-l1-4"]],
    "fr": [["fr-fun1-l1-0", "fr-fun1-l1-4", "fr-fun3-l1-2"], ["fr-fun1-l1-3", "fr-fun2-l1-5", "fr-fun3-l1-3"]],
    "es": [["es-fun1-l1-5", "es-fun1-l1-6", "es-fun2-l1-4"], ["es-fun2-l1-3", "es-fun1-l1-3", "es-fun2-l1-6"]],
    "it": [["it-fun1-l1-3", "it-fun1-l1-4", "it-fun1-l1-5"], ["it-fun1-l1-6", "it-fun2-l1-4", "it-fun2-l1-1"]],
}

def specs():
    ix = index(); out = {}
    def item(L, i, kind):
        w = ix[i]
        native = w.get("thai") if L == "th" else w.get("text") or w.get("thai")
        literal = (w.get("note") or "").replace("Word for word: ", "")
        return dict(path=audio(L, i), id=i, native=native, roman=w.get("roman", "") if L == "th" else "", en=w["en"], emoji=w.get("emoji", ""), literal=literal, kind=kind)
    for L in ("fr", "es", "it"):
        for t, (h, s, e, ids) in TOPICS.items():
            out[f"{L}-{t}"] = dict(lang=L, kind="phrases", hook=h.format(c=COUNTRY[L], l=LANG[L]), sub=s.format(c=COUNTRY[L], l=LANG[L]), emoji=e,
                                   items=[item(L, f"{L}-{i}", "phrase") for i in ids])
    for t, (h, s, e, ids) in THAI.items():
        out[f"th-{t}"] = dict(lang="th", kind="phrases", hook=h, sub=s, emoji=e, items=[item("th", i, "phrase") for i in ids])
    for L, groups in SAYINGS.items():
        for n, ids in enumerate(groups, 1):
            out[f"{L}-sayings{n}"] = dict(lang=L, kind="sayings", hook=f"{LANG[L]} sayings that make no sense in English", sub="3 real sayings, word for word 😂", emoji="🤯",
                                          items=[item(L, i, "saying") for i in ids])
    return out

if __name__ == "__main__":
    for k, v in specs().items():
        print(k, "|", v["hook"], "|", [(x["native"], x["en"]) for x in v["items"]])
