# Phase 4 — Review, Practice and Progress

Phase 3 is confirmed working: I signed in, played a lesson, and stars / XP / streak saved correctly. Thank you.

This phase builds the screens deferred from Phase 2 (the SRS scheduler and data helpers already exist — reuse them, don't change the scheduling rules or data model). Everything must use the Phase 3 visual identity (jade/marigold/lotus palette, Mitr + Sarabun, chunky press-down buttons, Nong Chang mascot, white 24–28px cards).

## 1. Review (spaced repetition)
- A **Review** button on the home screen, next to or under the "Next up" card, with a lotus badge showing how many words are due today.
- A review session = up to 15 due words, oldest-due first, using the same SessionPlayer and exercise types as each word's lesson tier (multiple-choice, listening, typing, match). Awards XP with source 'review' and updates word_srs exactly as lessons do.
- If nothing is due: a friendly card with the mascot — "You're all caught up — Nong Chang is proud of you" — and a button to start the next lesson.

## 2. Practice weak words
- A **Practice** button: 12 words with the lowest accuracy (at least 2 attempts), XP source 'practice'. If fewer than 4 qualify, say "Play a few more lessons first, then come back to practise your trickiest words."

## 3. Progress page (per profile)
Reachable from a header link. Mobile-first, works at 390px.
- Headline tiles: words learned (seen at least once), words mastered (interval ≥ 21 days), due today, current / longest streak.
- XP per day for the last 14 days — simple bar chart, marigold bars, today highlighted.
- 12-week activity heatmap (days with any XP) in jade shades.
- Accuracy by tone (mid / low / falling / high / rising) from word_srs counts joined with the curriculum's `tone`, so the learner sees which tones are hardest; show "Not enough answers yet" for tones with fewer than 5 attempts.
- Progress bar per level (lessons with ≥1 star / total).
- A friendly "Family this week" strip comparing each profile's XP this week (avatars, no rankings/medals).

## 4. Tidy-up
- Delete the temporary verification files `phase3-check.html` and `phase3-visual-check.tsx` from the project root.

## Verification
Add component tests for: review queue selection (due order, cap of 15, empty state), practice selection (min 2 attempts, lowest accuracy first), and the progress calculations (mastered count, tone accuracy). Don't create accounts — I'll check the real screens myself. Confirm the build passes and tell me in a few lines what changed.
