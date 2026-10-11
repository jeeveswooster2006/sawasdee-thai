# Phase 2 — full course content, real audio, spaced repetition, stats

Great work on Phase 1. This phase wires in the real content and adds the memory engine.

## 1. Load the full curriculum and recorded audio from the content CDN
The complete curriculum (6 levels, 43 units, 63 lessons, 352 words) and a recorded native-Thai mp3 for every word are published, byte-exact, at a pinned (immutable) commit:

- Content base: `https://cdn.jsdelivr.net/gh/jeeveswooster2006/sawasdee-thai@963dd43b13f8523629f4203ed41360c8eb00c4fe`
- Curriculum: `{base}/data/curriculum.json` (same structure as the bundled sample)
- Audio: `{base}/audio/{wordId}.mp3` — one file per word, named by the word's `id` (e.g. `b1-l1-0.mp3`)

Implementation:
- Put the base URL in one config constant (`CONTENT_BASE_URL`) so it can be bumped to a new commit later.
- On app start, fetch the curriculum; show a calm loading state (mascot + "Getting your lessons ready…"). Cache the fetched JSON in IndexedDB/localStorage keyed by the base URL, and use the cache instantly on later visits (refresh in the background).
- If the fetch fails and there's no cache, fall back to the bundled sample in `src/data/curriculum.json` and show a small dismissible banner: "Showing the first unit only — check your connection to load the full course."
- Never transform or edit the Thai text from the file.
- Audio service: `playThai(word)` now plays `{base}/audio/{word.id}.mp3` via a single reused `<audio>` element (preload the current exercise's clips). Only fall back to Web Speech th-TH if the file fails to load. Because real audio now exists for every word, listen-only exercises should always be available.
- Add a **slow-playback** button (turtle icon, 0.7× speed) next to every replay button.

## 2. Spaced repetition (the core of long-term memory)
Use the `word_srs` table. Implement an SM-2–style scheduler:
- Every time a word is answered in a lesson or review, grade it: correct first try = 5; correct after an earlier miss in the same session = 3; wrong = 1.
- Grade ≥ 3: repetitions += 1; interval = 1 day (first), 6 days (second), then round(interval × ease). Grade < 3: repetitions = 0, interval = 1 day, lapses += 1.
- ease = max(1.3, ease + (0.1 − (5 − grade) × (0.08 + (5 − grade) × 0.02))). Set due_at = now + interval days; keep correct_count / wrong_count / last_reviewed_at updated.
- Words enter the SRS the first time they appear in a completed lesson.

## 3. Review & practice modes
- **Review** (home screen button with a badge showing how many words are due): a session of up to 15 due words, oldest-due first, using the same exercise types as their lesson tier (mixed multiple-choice, listening, typing, match). Awards XP with source 'review'.
- **Practice weak words**: 12 words with the lowest accuracy (min. 2 attempts), source 'practice'.
- If nothing is due, show an encouraging empty state ("You're all caught up — Nong Chang is proud of you") with a button to start the next lesson.

## 4. Stats dashboard (per profile)
A "Progress" page reachable from the header:
- Headline tiles: words learned (seen at least once), words mastered (interval ≥ 21 days), due today, current/longest streak.
- XP per day for the last 14 days (simple bar chart, gold bars, today highlighted).
- 12-week activity heatmap (days with any XP), styled in the teal palette.
- Accuracy by tone (mid/low/falling/high/rising), computed from word_srs counts joined with the curriculum's `tone` field — this tells the learner which tones they find hardest.
- Progress bar per level (lessons with ≥1 star / total lessons).
- A "Family" strip comparing this week's XP for every profile on the account (friendly, not competitive-feeling).

## Quality bar
- Keep everything consistent with the established visual identity.
- Keyboard shortcuts work in review/practice too.
- No regressions to Phase 1 flows.
