# Phase 3 — fix the build, then the new look

The offline prototype has been retired; this app is now the only version. This phase (1) fixes the current build errors and (2) brings over the visual design and lesson feel we settled on. Review / Practice / Progress screens come in the next phase.

## 1. Fix the build first
The preview fails type-checking after Phase 2 (mostly `src/components/SessionPlayer.tsx`, plus `Avatars.tsx`, `CourseMap.tsx`, `ProfileForm.tsx` — possibly-null values). Fix these properly (narrowing / guards, not `any` or `!` everywhere), make sure the app builds and the existing tests pass, and verify a full lesson can be played start to finish.

## 2. Visual identity (replace the current cream/brown theme)
Palette inspired by Thai flower garlands and temple tiles. Define as CSS variables / Tailwind theme tokens, with a dark mode:

| token | light | dark |
|---|---|---|
| background | #eef5f0 (pale jade) | #0d1c1a |
| card | #ffffff | #152c29 |
| card-sunken | #e2ede6 | #10231f |
| ink (text) | #123b37 | #e6f3ef |
| ink-soft | #4f6b66 | #a9c4bd |
| line | #d3e3da | #24423d |
| jade (primary) | #0f8170, deep #0a5f53, soft #d3efe7 | #36c2a6 / #1f9a82 / #173d36 |
| marigold (XP, current, highlight) | #f2a024, deep #c97a06, soft #fdecc8 | #f6b84f / #d39226 / #3d3016 |
| lotus (hearts, accents) | #e0507a, soft #fbdbe5 | #f27b9c / #40202b |
| clay (wrong) | #c8432b, soft #f9ddd5 | #ef7a60 / #3f231c |
| sky / leaf (unit colours) | #3a72b8 / #5b9a2f | #79a7e4 / #8fcb61 |

Typography (Google Fonts, both cover Thai + Latin): **Mitr** (400/500/600) for headings, buttons, and every large Thai word; **Sarabun** (400–700) for body text. Body 17px.

Signature details:
- **Garland border** under the top bar: a repeating row of small dots — marigold, lotus, jade — like a phuang malai (CSS radial-gradients, ~36px repeat, 8px tall).
- **Chunky press-down buttons** for every primary action: 16px radius, solid fill, a 5px darker "ledge" (box-shadow 0 5px 0 deep shade) that collapses to 1px with translateY(4px) on press. Variants: jade (default), marigold (Start lesson), plain white with grey ledge (secondary).
- **Mascot**: use our illustrated Nong Chang image instead of the current drawn elephant: `https://cdn.jsdelivr.net/gh/jeeveswooster2006/sawasdee-thai@765fe4a518cc74a64fb640fdeaf8d01da0f4e386/art/mascot.png` (200×200, cream background — always show it inside a circle with a soft marigold ring). Use it in the header (40px), on sign-in, in the home hero, and on the lesson-complete screen.

## 3. Home / course map
- **Header**: mascot avatar + "Sawasdee Thai" (small pink "สวัสดี" above), profile switcher as a segmented pill, streak pill (clay on clay-soft) and XP pill (marigold on marigold-soft).
- **"Next up" hero card** at the top: mascot in a 148px circle gently bobbing, a tilted lotus speech bubble "สวัสดี!", eyebrow "Next up · Unit 4 · Family", the lesson title large, "6 new words for Dad.", a big marigold **Start lesson** button, and a progress meter for the current level ("Beginner · 7 / 28 lessons", jade→leaf gradient). When everything is done: "You finished every lesson, {name}!".
- **Levels** (Beginner, Elementary, Intermediate, Upper-Intermediate, Advanced, Fluency & Mastery) as collapsible sections; only the current level is open by default; the header shows "7 / 28 lessons" or "All 28 lessons done ✓".
- **Unit cards**: white, 24px radius, soft shadow. Each unit gets a colour cycling jade → marigold → lotus → sky → leaf. A **banner** at the top (128px; 76px once the unit is finished; 70px and greyscale while locked) shows the unit illustration from `https://cdn.jsdelivr.net/gh/jeeveswooster2006/sawasdee-thai@main/art/units/{unitId}.webp` (object-fit cover). Most don't exist yet — if the image fails to load, hide it and show the unit's **first Thai word** as a huge faded watermark (Mitr 600, ~6rem, unit colour at 20% opacity, bleeding off the bottom-right). "Unit N" chip top-left, "Done ✓" chip top-right when finished. Below: title, tagline, then the lessons as **stepping stones** in a row joined by a dotted line: 66px rounded stones with the 3D ledge — done = filled unit colour with ✓ and ★★☆ under it, available = soft unit colour with the number, current = marigold with a small bobbing "Start" tag above it, locked = grey 🔒. Locked units show only the title/tagline and, for the first locked one, "🔒 Finish “Family” to open this unit".

## 4. Lesson screen
- Top: ✕ exit, a thick 16px jade progress bar with a white highlight stripe (springy width transition), lotus hearts.
- The exercise sits in a white 28px-radius card. Prompt: Thai word very large (Mitr, ~3.4rem) with romanisation under it; English prompts in Mitr ~2.2rem; listening prompts show a faded "· · ·" instead of the word.
- Audio: a round 58px jade 🔊 button and a smaller soft-jade 🐢 slow button beside it.
- **Answer options** as chunky white cards with a 2px border and 4px ledge, each with a small numbered key badge (1, 2, 3…) on the left. Selected = marigold border + marigold-soft fill; correct = jade; wrong = clay (key badge fills with the colour). Unchosen options fade after checking.
- **Keyboard**: 1–9 picks an option, Enter checks / continues (not while typing in an input, where Enter submits).
- Check button: full-width chunky jade, disabled state grey.
- **Feedback sheet**: after checking, a panel slides up from the bottom of the screen (fixed, full width, content aligned to the lesson column): jade-soft "Nice!" / "เก่งมาก! Great!" / "Correct!" (random), or clay-soft "Not quite" with the correct answer underneath (English — Thai (roman)). Keep the existing timing/flow.
- Match round tiles use the same chunky style; solved pairs shrink slightly and fade.

## 5. Lesson complete
White card: the mascot in a 150px circle that hops twice, "Perfect lesson!" / "Great job!" / "Lesson complete", three big stars that pop in one after another (unearned stars stay grey), an XP chip "+80 XP", buttons "Do it again" (plain) and "Continue" (jade). Out of hearts: the same card, mascot with a lotus ring and no hop, "Out of hearts", "Take a breath and try this lesson again. You'll remember more the second time.", "Lesson map" / "Try again". Confetti in the palette colours on success.

## Quality bar
- Respect prefers-reduced-motion (no bobbing/hopping/confetti), visible keyboard focus (3px marigold outline), works at 390px wide (hero stacks and centres, Start button full width).
- Don't change the data model, SRS logic, or content loading from Phase 2.
- When done, tell me in a few lines what you changed, and confirm the build passes.
