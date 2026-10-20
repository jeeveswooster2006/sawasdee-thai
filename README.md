# Natterly — learn Thai together as a family

**Try the app: [sawasdee-family.lovable.app](https://sawasdee-family.lovable.app)** · [How it works](https://sawasdee-family.lovable.app/learn-thai)

Natterly (formerly Sawasdee Thai) is a free, family-friendly Thai course for grown-ups and kids: short lessons, Thai audio for every word, a kids' mode, a Read Thai track for the alphabet and tones, and Nong Chang the baby elephant cheering you on.

This repository holds the course content the app uses: the curriculum (`data/curriculum.json`), Thai audio (`audio/`) and the illustrations (`art/`).

---

## Original offline version

A Duolingo-style Thai course for two learners, built to run entirely on your own PC.

## How to open it

Double-click **`index.html`**. It opens straight in your default browser — no install, no server, no account. Keep the `audio` folder next to `index.html`: it holds the recorded pronunciation for every word.

Everything works offline after the first load. The only thing that needs the internet is the Google Fonts stylesheet; if you're offline it just falls back to your system font.

## What's inside

- **43 units, 63 lessons**, beginner all the way through fluency:
  - **Beginner** (14 units, 28 lessons): greetings, numbers, family, colors & shapes, food & drink, everyday phrases, time & days, places & directions, shopping, travel, weather, feelings & health, and full sentences.
  - **Elementary** (6 units, 9 lessons): classifiers (Thai's "counter word" system), daily routine & time-of-day, tense markers (จะ / กำลัง / แล้ว / เคย), comparisons, ordering at a restaurant, and making plans.
  - **Intermediate** (6 units, 9 lessons): connectors (and/but/because/if), giving directions in full sentences, describing people, work & occupations, short back-and-forth conversations, and health/emergency phrases.
  - **Upper-Intermediate** (6 units, 6 lessons): opinions & agreement, abstract ideas (happiness, success, goals), storytelling connectors, formal titles & address, phone conversations, and everyday idioms.
  - **Advanced** (5 units, 5 lessons): business Thai, news & society vocabulary, passive voice & relative clauses, classic Thai proverbs, and discussion/debate language.
  - **Fluency & Mastery** (6 units, 6 lessons): slang & casual speech, humor & reactions, reading a connected paragraph, casual everyday greetings, formal/professional register, and literary vocabulary from songs and poetry.
- **Gets harder as you go**: early units are simple multiple-choice recognition; the middle units add listening challenges and a matching round; later units add typing exercises and full sentences; elementary-and-up units add listen-and-type challenges with no text shown at all.
- **Hearts & XP**, like Duolingo: 5 hearts per lesson, lose one per mistake, run out and you retry; earn XP and stars (1–3) per lesson, plus a day streak.
- **Two profiles** — Dad and Son buttons in the top bar — each with completely separate progress, saved on this PC via the browser's local storage.
- **Recorded Thai pronunciation for all 352 words** — a native-sounding Thai voice, with a Play and a 🐢 Slow button on every Thai prompt. Wrong answers play the correct word, and tapping a Thai tile in the matching round plays it too.

## Notes

- Progress is stored per-browser, per-profile. If you switch browsers or clear site data, progress for that browser resets.
- If the `audio` folder is missing (for example, only `index.html` was copied), the app falls back to your browser's built-in Thai voice where one exists.
- Want more lessons, a different difficulty curve, or new units? Just ask — the whole curriculum lives in one readable block near the top of `index.html`.
