import json, specs
SP = specs.specs()
L = specs.LANG
order = ["fr-sayings1","th-basics","es-shopping","it-sayings1","fr-basics","th-sayings1","es-stuck","it-shopping",
         "es-sayings1","fr-stuck","th-market","it-basics","fr-sayings2","es-basics","it-stuck","th-sayings2",
         "fr-shopping","es-directions","it-sayings2","th-directions","fr-directions","fr-emergency","it-directions",
         "th-help","es-sayings2","es-emergency","it-emergency"]
assert sorted(order) == sorted(SP)
TOPIC = {"shopping": "for shopping", "basics": "to learn first", "stuck": "for when you're stuck", "directions": "for finding your way",
         "emergency": "for an emergency", "market": "for haggling at the market", "help": "for an emergency"}
# Two a day (Paul, 26 Nov): mornings 08:00 from 27 Nov (18:00 holds the restaurant pilots until 30 Nov), then 08:00 + 17:00 from 1 Dec. UK = UTC in winter.
SLOTS = [f"2026-11-{d}T08:00:00Z" for d in (27, 28, 29, 30)] + [f"2026-12-{d:02d}T{h}:00:00Z" for d in range(1, 13) for h in ("08", "17")]
rows = []
for i, k in enumerate(order):
    s = SP[k]; lang = L[s["lang"]]; f = specs.FLAG[s["lang"]]
    if s["kind"] == "sayings":
        title = f"3 {lang} sayings that make no sense in English {f} #shorts"
        tags = [f"{lang} sayings", f"{lang} idioms", f"learn {lang}", f"{lang} expressions", "idioms", "language learning"]
    else:
        n = len(s["items"]); topic = k.split("-")[1]
        title = f"{n} {lang} phrases {TOPIC[topic]} {f} #shorts"
        tags = [f"{lang} phrases", f"learn {lang}", f"{lang} for travel", f"{specs.COUNTRY[s['lang']]} travel", "travel phrases", "language learning"]
    lines = "\n".join(f"• {x['native']}" + (f" ({x['roman']})" if x['roman'] else "") + (f" = word for word “{x['literal']}”, really “{x['en']}”" if x['kind']=='saying' else f" = {x['en']}") for x in s["items"])
    desc = f"{s['hook']} {s['sub']}.\n\n{lines}\n\nNative speaker recordings. Say it out loud in the pause!\n\nLearn {lang} (and Thai, French, Spanish, Italian, English) together as a family, free with no ads: nongchang.co.uk/yt"
    at = SLOTS[i]
    rows.append(dict(key=k, date=at[:16].replace("T", " "), publishAt=at, title=title, tags=tags, description=desc))
json.dump(rows, open("plan.json", "w"), ensure_ascii=False, indent=1)
for r in rows: print(r["date"], r["key"].ljust(14), r["title"])
