"""Recording batches for the Read Thai track (letters, vowels, tones, tone marks).

Item ids and spoken text match src/data/read-thai.ts in the app (say = letter + อ + name for letters,
the written form for the rest). Clips are saved as audio/{id}.mp3; items that share a sound share a clip.
"""
import json

MID = [("ก","ไก่"),("จ","จาน"),("ด","เด็ก"),("ต","เต่า"),("บ","ใบไม้"),("ป","ปลา"),("อ","อ่าง"),("ฎ","ชฎา"),("ฏ","ปฏัก")]
HIGH = [("ข","ไข่"),("ฉ","ฉิ่ง"),("ถ","ถุง"),("ผ","ผึ้ง"),("ฝ","ฝา"),("ศ","ศาลา"),("ษ","ฤๅษี"),("ส","เสือ"),("ห","หีบ"),("ฐ","ฐาน"),("ฃ","ขวด")]
LOW = [("ค","ควาย"),("ง","งู"),("ช","ช้าง"),("ซ","โซ่"),("ท","ทหาร"),("น","หนู"),("พ","พาน"),("ฟ","ฟัน"),("ม","ม้า"),("ย","ยักษ์"),
       ("ร","เรือ"),("ล","ลิง"),("ว","แหวน"),("ฮ","นกฮูก"),("ฅ","คน"),("ฆ","ระฆัง"),("ฌ","เฌอ"),("ญ","หญิง"),("ฑ","มณโฑ"),
       ("ฒ","ผู้เฒ่า"),("ณ","เณร"),("ธ","ธง"),("ภ","สำเภา"),("ฬ","จุฬา")]
VOWELS = ["อะ","อา","อิ","อี","อุ","อู","เอะ","เอ","แอ","โอ","ไอ","ใอ","อำ"]
TONES = [("mid","กา"),("low","ก่า"),("falling","ก้า"),("high","ก๊า"),("rising","ก๋า")]
MARKS = [("gaa","กา"),("ek","ก่า"),("tho","ก้า"),("tri","ก๊า"),("chattawa","ก๋า"),("maa","มา"),("maa-ek","ม่า"),
         ("maa-tho","ม้า"),("khaa","ขา"),("khaa-ek","ข่า"),("khaa-tho","ข้า")]

items = [(f"rt-letter-{t}", f"{t}อ {n}") for t, n in MID + HIGH + LOW]
items += [(f"rt-vowel-{v}", "ไอ" if v == "ใอ" else v) for v in VOWELS]   # ไอ and ใอ sound the same
items += [(f"rt-tone-{k}", s) for k, s in TONES] + [(f"rt-mark-{k}", s) for k, s in MARKS]
assert len(items) == 73

shared = {}
for i, s in items:
    shared.setdefault(s, []).append(i)
unique = list(shared)                      # spoken texts, in first-seen order
letters, rest = unique[:44], unique[44:]
groups = []
for g, chunk in enumerate([letters[:22], letters[22:], rest]):
    groups.append({"group": g, "ids": [shared[s][0] for s in chunk], "texts": chunk,
                   "prompt": "[slowly, clearly] " + " ... ".join(chunk)})
json.dump(groups, open("audio_groups.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({shared[s][0]: shared[s][1:] for s in unique if len(shared[s]) > 1}, open("copies.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print(len(items), "items,", len(unique), "recordings,", sum(len(g["prompt"]) for g in groups), "prompt chars")
for g in groups: print(g["prompt"], "\n")
