# Next Lovable job: lesson fixes (prepared 28 Oct 2026)

Exact code locations were checked in the Lovable project (commit c997890) so the agent doesn't need to search. Expected cost: about 1–2 credits (small, local edits).

## Message to send

> Lesson fixes. Keep it small: only these changes, and only update or add tests where these files need it.
>
> 1. **Spanish lessons show Thai wording.** Use `courseOfId(word.id)` from src/lib/content.ts:
>    a. src/components/SessionPlayer.tsx, `Prompt()`: the title for "en-to-thai" is "Pick the Thai"; use "Pick the Spanish" for Spanish words.
>    b. SessionPlayer feedback praise `["Nice!", "เก่งมาก! Great!", "Correct!"]`: for Spanish words use "¡Muy bien! Great!" instead of the Thai one.
>    c. src/lib/kids-mode.ts `CHEERS` includes "เก่งมาก! Great job!": for Spanish use "¡Muy bien! Great job!" (let `kidCheer` take the course).
>    d. Spanish text is rendered with `lang="th"` and `font-thai` (ThaiWord, the en-to-thai option buttons, the "Not quite" line, MatchRound's left tiles): use `lang="es"` and the normal body font for Spanish words.
> 2. **Questions give the answer away.** src/lib/kids-mode.ts `promptEmoji` returns the word's emoji for "thai-to-en" and "type-en", so the picture above the Thai word matches the correct option (👋 above สวัสดี with the option "👋 Hello"; "50" above ห้าสิบ with "50 Fifty"). Return `undefined` for those two types (keep "en-to-thai", where the prompt is English). Emojis still show on the options, in the "Not quite" feedback and on intro cards.
> 3. **Report flag looks broken on phones.** src/components/ReportWordButton.tsx: when `reported` is true the flag is only disabled with a hover title, which phones never show. Show a small green check with the word "Reported" instead (still not clickable).
> 4. **Content update.** src/lib/content.ts: set CONTENT_BASE_URL to commit `e98ee2788864210ef3dc607f76e718039606d902`. In that content, Thai multi-syllable words whose syllables have different tones now have `tone: ""` (ThaiWord already hides the badge when tone is empty) plus a new optional `tones: string[]` (one per syllable); make sure nothing breaks with an empty tone (tone stats should skip it).
>
> Run the typecheck and the tests for these files. Don't publish.
