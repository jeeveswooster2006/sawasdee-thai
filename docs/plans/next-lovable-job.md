# Next Lovable jobs (updated 29 Oct 2026)

**Job 1 (lesson fixes): DONE and published 29 Oct** (Lovable commit f168bc6, cost 2.5 credits against an estimate of 1). Lovable jobs cost about 2–3× my first guess, so plan for that.

**Job 2 (languages come from the content) is split in two**, one per day:
- **Job 2a, about 3–4 credits:** sections 1, 2 and 4 of the message below (live.json pointer, courses.json language list, database check). Add to the message: "Do sections 1, 2 and 4 only; section 3 comes in a later job. Keep the current Thai/Spanish wording code working."
- **Job 2b, about 2–3 credits:** section 3 (pick label, praise, cheer, language and font, spoken fallback, the Say-it language) plus section 5's tests for it.
- Before sending Job 2a, re-check src/lib/content.ts in Lovable (it now pins content commit 7542ff8).

## Job 1: message that was sent (done)

> Lesson fixes. Keep it small: only these changes, and only update or add tests where these files need it.
>
> 1. **Questions give the answer away.** src/lib/kids-mode.ts `promptEmoji` returns the word's emoji for "thai-to-en" and "type-en", so the picture above the Thai word matches the correct option (👋 above สวัสดี with the option "👋 Hello"; "50" above ห้าสิบ with "50 Fifty"). Return `undefined` for those two types (keep "en-to-thai", where the prompt is English). Emojis still show on the options, in the "Not quite" feedback and on intro cards.
> 2. **Report flag looks broken on phones.** src/components/ReportWordButton.tsx: when `reported` is true the flag is only disabled with a hover title, which phones never show. Show a small green check with the word "Reported" instead (still not clickable).
> 3. **Content update.** src/lib/content.ts: set CONTENT_BASE_URL to commit `4e0c2da2b1937e3af447ffc5c3755ebcf6569ea6`. In that content, Thai multi-syllable words whose syllables have different tones now have `tone: ""` (ThaiWord already hides the badge when tone is empty) plus a new optional `tones: string[]` (one per syllable); make sure nothing breaks with an empty tone (tone stats should skip it).
>
> Run the typecheck and the tests for these files. Don't publish.

## Job 2: message to send

> Make languages come from the content repo, so adding a language never needs an app change. Keep Thai and Spanish working exactly as now. Don't publish.
>
> **1. Which content is live.** On the client, at start-up, fetch `https://raw.githubusercontent.com/jeeveswooster2006/sawasdee-thai/main/live.json` (`cache: "no-store"`, 3-second timeout). It looks like `{"content": "<40-hex commit>"}`.
> - The content base becomes `https://cdn.jsdelivr.net/gh/jeeveswooster2006/sawasdee-thai@<that commit>`.
> - Keep the current `CONTENT_BASE_URL` as the built-in fallback. Use it when the fetch fails, times out or isn't a 40-hex hash, and on the server render.
> - Remember the last good commit in localStorage and use it straight away on the next visit, refreshing in the background (a new value applies on the next load).
> - If the page URL has `?content=<40-hex>`, use that commit for this browser tab (sessionStorage), so new content can be checked on the preview before it goes live.
> - Everything that builds content URLs (curriculumUrl, audioUrl, unitArtUrl, mascotImageUrl, curriculumCacheKey, Read Thai audio) must use this base.
>
> **2. The language list.** Load `<content base>/courses.json` (cache it like the curriculum).
> - It's an array of courses with: id, name, native, flag, mascot, speechLang, curriculum, audio, art, mascotImage, and optional extraTrack/extraTrackFile.
> - New fields:
>   - `idPrefix`: "" for Thai, "es-" for Spanish.
>   - `lang`: the HTML lang code.
>   - `script`: "thai" or "latin".
>   - `pickLabel`: e.g. "Pick the Spanish".
>   - `praise`: e.g. "¡Muy bien! Great!".
>   - `cheer`: e.g. "¡Muy bien! Great job!".
>   - `hidden`: optional boolean.
> - Replace the hard-coded `COURSES`, `COURSE_IDS` and the `"th" | "es"` `CourseId` type in src/lib/content.ts with this list (`CourseId` becomes `string`). Keep the current Thai and Spanish entries, with the new fields, as the built-in fallback.
> - `isCourseId` checks the loaded list.
> - `courseOfId(id)` returns the course whose non-empty `idPrefix` the id starts with (longest match), otherwise the course with an empty prefix (Thai).
> - The LanguageMenu in src/components/AppHeader.tsx already lists `COURSE_IDS`. Courses with `hidden: true` must not be offered under "Add …", except on the Lovable preview host or when a `?content=` override is active, where they show with "(preview)". A learner who already has a hidden course keeps it.
>
> **3. Use the list's fields instead of Thai/Spanish checks.** Search for `=== "es"`, `=== "th"`, `"es-"`, `speechPrefixFor`, `COURSE_IDS` and `font-thai`.
> - **Pick label:** src/components/SessionPlayer.tsx `Prompt()` uses the word's course `pickLabel` instead of "Pick the Thai".
> - **Praise and cheer:** the SessionPlayer praise `["Nice!", "เก่งมาก! Great!", "Correct!"]` uses the course `praise` in place of the Thai one. src/lib/kids-mode.ts `CHEERS` uses the course `cheer` in place of "เก่งมาก! Great job!" (`kidCheer` takes the course).
> - **Language and font:** words are rendered with `lang` = the course `lang`, and `font-thai` only when `script` is "thai", otherwise the normal body font. This covers ThaiWord, the en-to-thai option buttons, the "Not quite" line and MatchRound's left tiles.
> - **Spoken fallback:** src/lib/audio.ts uses the course `speechLang` (language part) for the browser-voice fallback, and the 0.85 rate only for Thai.
> - **"Say it" exercise:** src/lib/speech.ts `createRecognizer` takes a language and uses the active course `speechLang`. It is hard-coded to "th-TH" today, so Spanish "Say it" listens for Thai.
> - Thai-only features stay keyed on "th": the Read Thai tab, starting level and placement test, tone drills, romanisation, and the Thai font setting.
>
> **4. Database.** Add a migration that replaces the fixed `('th','es')` lists with a format check `~ '^[a-z]{2,3}$'`:
> - the check constraints on `learner_profiles.active_course` and `learner_courses.course` (look up their real names);
> - the checks inside `set_active_course` and `set_course_start_level`.
>
> Keep everything else in those functions the same.
>
> **5. Tests.**
> - `courseOfId` with a three-course list (th, es, and a made-up "fr" with prefix "fr-").
> - The live.json fallback when the fetch fails.
> - A hidden course not being offered outside the preview.
>
> Run the typecheck and all tests. Don't publish.

## After Job 2 is published

- **Releasing content:** commit to main, then change `live.json` to that commit. The live app picks it up on the next load, with no Lovable credits.
  - Moving `live.json` counts as publishing: only do it when Paul says "publish".
  - To check first, open the Lovable preview with `?content=<commit>`.
- **Launching French:**
  1. Finish the recordings and unit pictures.
  2. Remove `"hidden": true` from the French entry in courses.json.
  3. Commit, then move `live.json` (after Paul says "publish").
