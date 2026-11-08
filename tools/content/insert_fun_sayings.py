# Adds the 3 bonus "Fun sayings" units to the end of the first three levels of each course (idempotent).
import json, sys
D = "/tmp/claude-0/-home-user/e3a27352-eabf-5796-b70f-fdffad55ed6a/scratchpad/idioms/draft.json"
R = "/home/user/sawasdee-thai/"
PATHS = {"th": "data/curriculum.json", "es": "courses/es/curriculum.json", "fr": "courses/fr/curriculum.json", "it": "courses/it/curriculum.json"}
draft = json.load(open(D))
for lang, path in PATHS.items():
    raw = open(R + path).read()
    second = raw.split("\n")[1] if "\n" in raw else ""
    indent = (len(second) - len(second.lstrip(" "))) or None
    levels = json.loads(raw)
    for i, unit in enumerate(draft[lang]):
        lv = levels[i]
        lv["units"] = [u for u in lv["units"] if u["id"] != unit["id"]] + [unit]
    with open(R + path, "w") as f:
        json.dump(levels, f, ensure_ascii=False, indent=indent)
        if raw.endswith("\n"): f.write("\n")
    print(lang, [ (lv["level"], lv["units"][-1]["id"]) for lv in levels[:3]])
