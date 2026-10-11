# Sawasdee Thai — a family Thai-learning app (Phase 1 of 6)

## What we're building
A polished, Duolingo-quality Thai course for a parent and child (age 7–12) who learn together. Duolingo has no Thai course — this app fills that gap and should feel like a real, premium product: fast, delightful, motivating, and genuinely good at teaching.

A working prototype already exists (single offline HTML file). This project is the full rebuild: real accounts, cloud-synced progress across devices, and a much richer learning engine. The complete curriculum is provided below — 6 levels, 43 units, 63 lessons, 352 Thai words/phrases.

## Phase plan (so you can design for what's coming)
1. **This message:** accounts + learner profiles, course map, lesson engine, XP/hearts/streak/daily goal, progress synced to the database.
2. Spaced-repetition reviews (per-word memory model), "practice weak words", stats dashboard.
3. Real recorded audio per word (mp3 files at `/audio/{wordId}.mp3` — coming later; build the audio service now with a fallback), slow-playback mode, tone-identification drills, sentence builder with word tiles.
4. Speaking practice (Web Speech API, th-TH), achievements/badges, weekly family leaderboard, streak freezes.
5. Installable PWA with offline lessons.
6. Custom illustrations: mascot + one illustration per unit.

## Phase 1 scope

### Accounts & learner profiles
- Email + password sign-in (one account per family).
- After sign-in, a profile picker ("Who's learning?") with big avatar tiles. Create profiles with a name, an avatar (pick from a set of 8 friendly animal avatars rendered as simple illustrations — no emoji), and a daily goal (Casual 10 XP / Regular 20 XP / Serious 50 XP). Seed suggestion: "Dad" and "Son".
- Switching profile is one tap from the header. All progress is per profile.

### Database (use the built-in backend)
Create these tables with row-level security so an account only ever sees its own profiles' data:
- `learner_profiles`: id, account_id (auth user), name, avatar, daily_goal_xp, created_at
- `lesson_progress`: profile_id, lesson_id, best_stars (0–3), completions, best_accuracy, last_completed_at — unique (profile_id, lesson_id)
- `word_srs`: profile_id, word_id, ease (default 2.5), interval_days, repetitions, lapses, due_at, last_reviewed_at, correct_count, wrong_count — unique (profile_id, word_id). Phase 2 uses this; in Phase 1 just upsert correct/wrong counts and last_reviewed_at whenever a word is answered.
- `xp_events`: profile_id, amount, source ('lesson' | 'review' | 'practice'), created_at
- `streaks`: profile_id (unique), current_streak, longest_streak, last_active_date, freezes_available (default 0)

### Course map
- Duolingo-style vertical winding path. Six levels (Beginner → Fluency & Mastery), each with a level header; units show a banner with title + tagline; lessons are circular nodes that zig-zag down the path.
- Node states: locked (dimmed + lock), available, current (gently pulsing, "Start" bubble), completed (filled, shows 1–3 stars).
- Unlocking: lesson N+1 unlocks when lesson N has ≥1 star; the first lesson of a unit unlocks when every lesson of the previous unit has ≥1 star.
- Clicking an available node opens a small popover: lesson title, words-in-lesson count, best stars, "Start" button.
- Header: profile avatar/switcher, streak flame with count, total XP, daily-goal progress ring.

### Lesson engine
Build a queue of exercises from the lesson's words, scaled by difficulty tier. Tier by unit position across the whole course (0-indexed across all 43 units): units 0–3 tier 1, 4–7 tier 2, 8–13 tier 3, 14+ tier 4.
- Tier 1: for each word — "Thai → pick English" and "English → pick Thai" multiple choice, 3 options.
- Tier 2: add 2 "Listen → pick meaning" exercises (audio only, no text) and use 4 options.
- Tier 3: add 2 "Type the English meaning" exercises.
- Tier 4: add 2 "Listen and type the meaning" exercises (audio only, typed answer).
- Every lesson with ≥3 words ends with a "Match the pairs" round (tap a Thai tile then its English tile).
- **Distractors:** draw wrong options from the same lesson first; only fall back to earlier lessons' words if the lesson doesn't have enough. (Mixing a full sentence with single-word distractors makes questions guessable by shape — avoid that.)
- **Typed answers:** compare case-insensitively, ignoring punctuation and extra spaces, against the word's `en` and every entry in its `accept` array.
- Shuffle the queue; match round always last.
- **Hearts:** 5 per lesson; a wrong answer costs one; at 0 the lesson ends with an "Out of hearts — try again" screen.
- **Feedback:** after "Check", a bottom sheet slides up — green "Nice!" or red "Correct answer:" with the Thai, romanization, English and a replay button. Wrong answers are re-queued once at the end of the lesson (like Duolingo) so the learner sees them again.
- **Combo:** show a small combo counter after 3+ correct in a row.
- **Display:** Thai script large (Noto Sans Thai), romanization below it, and a small colored tone chip (mid/low/falling/high/rising — use the `tone` field). Color-swatch words (`swatch` field) show the color.
- **Keyboard shortcuts:** 1–4 pick options, Enter = check/continue, Space = replay audio. Show the shortcut hints subtly on desktop.
- **Results screen:** stars (3 = no mistakes, 2 = ≤2 mistakes, 1 = finished), XP earned (10 per correct answer + 20 for the match round + 10 bonus for a perfect lesson), accuracy %, time taken, celebratory confetti; buttons "Continue" (back to map, scrolled to next lesson) and "Practice again".
- Record XP events, update lesson_progress (keep best), upsert word stats, update the streak (consecutive days with ≥1 lesson; a missed day resets to 1).
- XP and streak in the header must update immediately after a lesson.

### Audio service (build now, real files arrive in Phase 3)
- `playThai(word)`: try `/audio/{word.id}.mp3`; if it fails to load, fall back to the Web Speech API with a th-TH voice; if no Thai voice exists, show a quiet "No Thai voice on this device" toast once and disable listen-only exercise types for the session (replace them with read exercises so lessons still work).
- `playEnglish(text)`: Web Speech API en voice.
- Auto-play the Thai audio when a Thai prompt appears; replay button on every Thai prompt.

### Visual identity — important
Not a Duolingo clone and not a generic template. The identity is drawn from Thai temple mosaic and lacquerware:
- Palette: warm ivory ground `#F6EFE0`, raised surfaces `#FFFAF0`, deep teal `#145952` (primary/success), temple gold `#B3801F` (highlights, current node, stars, XP), vermilion `#B5502F` used only for errors, ink `#241B12`. Dark mode: lacquer black `#1A1611` ground, gold `#E0AB4A`, teal `#5FC2B4`.
- A thin repeating gold/teal dashed trim (like temple tile edging) under the header — the one signature decorative element; keep everything else calm.
- Type: "Baloo 2" for headings and UI numbers, "Work Sans" for body, "Noto Sans Thai" for all Thai text. Thai text must never fall back to a font that renders it poorly.
- Chunky, tactile buttons with a bottom "press" shadow (3D press on click), rounded but not pill-everything.
- Mascot (placeholder until Phase 6): "Nong Chang", a friendly baby elephant — Thailand's national animal. Use a simple, tasteful SVG placeholder on the welcome screen, results screen and empty states.
- Motion: snappy and purposeful — node pulse, bottom-sheet slide, confetti on results, heart shake on mistake. Respect prefers-reduced-motion.
- Fully responsive: excellent on a phone and on a desktop browser. Visible focus states for keyboard users.

### Copy tone
Warm, encouraging, plain. Short sentences. Buttons say exactly what happens ("Check", "Continue", "Try again"). Errors explain what to do next.

## Curriculum data
The full curriculum (6 levels, 43 units, 63 lessons, 352 words) lives in `src/data/curriculum.json`. I will commit the real file directly to the repository byte-for-byte via GitHub so no Thai text gets altered in transit — **never hand-edit, retype, translate or "fix" any Thai text, romanization, tone or English in that file.**

For now, create `src/data/curriculum.json` containing exactly this sample (the first unit), and build everything to read from that file generically (any number of levels/units/lessons/words), so the app works unchanged when the full file lands:

Structure: `[{ level, units: [{ id, title, tagline, lessons: [{ id, title, words: [{ id, thai, roman, en, tone, accept?, swatch? }] }] }] }]`. Each word's `id` is stable and is used for audio filenames and progress tracking.

```json
[
  {
    "level": "Beginner",
    "units": [
      {
        "id": "basics1",
        "title": "Greetings",
        "tagline": "The words you'll use every single day.",
        "lessons": [
          {
            "id": "b1-l1",
            "title": "Hello & thanks",
            "words": [
              {
                "id": "b1-l1-0",
                "thai": "สวัสดี",
                "roman": "sa-wàt-dii",
                "en": "Hello",
                "tone": "falling",
                "accept": [
                  "hello",
                  "hi",
                  "goodbye",
                  "bye"
                ]
              },
              {
                "id": "b1-l1-1",
                "thai": "ขอบคุณ",
                "roman": "khɔ̀ɔp-khun",
                "en": "Thank you",
                "tone": "low",
                "accept": [
                  "thank you",
                  "thanks"
                ]
              },
              {
                "id": "b1-l1-2",
                "thai": "ใช่",
                "roman": "châi",
                "en": "Yes",
                "tone": "falling"
              },
              {
                "id": "b1-l1-3",
                "thai": "ไม่ใช่",
                "roman": "mâi châi",
                "en": "No",
                "tone": "falling"
              },
              {
                "id": "b1-l1-4",
                "thai": "ขอโทษ",
                "roman": "khɔ̌ɔ-thôot",
                "en": "Sorry",
                "tone": "rising",
                "accept": [
                  "sorry",
                  "excuse me"
                ]
              },
              {
                "id": "b1-l1-5",
                "thai": "ไม่เป็นไร",
                "roman": "mâi-pen-rai",
                "en": "No worries",
                "tone": "mid",
                "accept": [
                  "no worries",
                  "you're welcome",
                  "never mind"
                ]
              }
            ]
          },
          {
            "id": "b1-l2",
            "title": "How are you?",
            "words": [
              {
                "id": "b1-l2-0",
                "thai": "สบายดีไหม",
                "roman": "sa-baai-dii mǎi",
                "en": "How are you?",
                "tone": "rising"
              },
              {
                "id": "b1-l2-1",
                "thai": "สบายดี",
                "roman": "sa-baai-dii",
                "en": "I'm fine",
                "tone": "mid",
                "accept": [
                  "i'm fine",
                  "im fine",
                  "fine",
                  "good"
                ]
              },
              {
                "id": "b1-l2-2",
                "thai": "ยินดีที่ได้รู้จัก",
                "roman": "yin-dii thîi dâai rúu-jàk",
                "en": "Nice to meet you",
                "tone": "falling"
              },
              {
                "id": "b1-l2-3",
                "thai": "ครับ",
                "roman": "khráp",
                "en": "Polite word (male)",
                "tone": "high",
                "accept": [
                  "polite word (male)",
                  "polite particle male",
                  "male polite word"
                ]
              },
              {
                "id": "b1-l2-4",
                "thai": "ค่ะ",
                "roman": "khâ",
                "en": "Polite word (female)",
                "tone": "falling",
                "accept": [
                  "polite word (female)",
                  "polite particle female",
                  "female polite word"
                ]
              },
              {
                "id": "b1-l2-5",
                "thai": "ราตรีสวัสดิ์",
                "roman": "raa-trii sa-wàt",
                "en": "Good night",
                "tone": "falling"
              }
            ]
          }
        ]
      }
    ]
  }
]
```

Please build Phase 1 completely and to a high standard — this is the foundation everything else sits on.
