Please continue Phase 3 from where you stopped (same brief, same plan in .lovable/plan.md):

1. **Fix the remaining type errors** in `src/components/SessionPlayer.tsx` (and anything else still failing) with proper guards, until the build passes and the existing tests pass.
2. **Finish the lesson screens in the new design** (brief sections 4 and 5): the white exercise card with the very large Thai prompt, round 🔊 / smaller 🐢 buttons, chunky numbered answer options (selected = marigold, correct = jade, wrong = clay), 1–9 / Enter keyboard shortcuts, the slide-up feedback sheet, chunky match tiles, and the lesson-complete / out-of-hearts cards with the hopping mascot, popping stars and XP chip.
3. **Verify** without needing a real sign-in: use your existing tests plus a component-level test that plays a short lesson to the end (correct and wrong answers, hearts, completion screen). Don't create accounts — I'll sign in and check saved progress myself.

Keep the data model, SRS logic and content loading unchanged. When done, tell me in a few lines what changed and confirm the build passes.
