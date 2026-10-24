# Fixes from Reddit feedback (send to Lovable 25 Oct 2026)

Feedback from a beginner on r/learnthai:
1. Thai is shown in a modern (loopless) font; learners need a traditional looped font by default, with an option to switch.
2. Let learners hide the transcription and reveal it only when needed (e.g. a small ⓘ to tap).
3. No obvious way to change the starting level later (it only exists as a small link on the Learn page).
4. On a laptop at 100% zoom the four multiple-choice answers don't fit; the learner has to scroll.

Send as two jobs and check the cost after the first. Expected ~1.5 credits each.

---

## Job A: traditional Thai font + "tap to reveal" transcription

> Two small display settings from user feedback. Keep it tight; no other changes, no database changes.
>
> **1. Traditional (looped) Thai font by default.** Lessons currently show Thai in Mitr, a loopless modern font, which is harder for learners. In `src/styles.css`:
> - add to `:root`: `--thai-face: "Sarabun", ui-sans-serif, system-ui, sans-serif;` (Sarabun is the looped font the app already loads, weights 400–700)
> - add `:root[data-thai-font="modern"] { --thai-face: "Mitr", "Sarabun", sans-serif; }`
> - change `--font-thai` in `@theme inline` to `var(--thai-face)`, the `:lang(th), .thai` rule to `font-family: var(--thai-face)`, and `@utility font-thai` to `font-family: var(--thai-face); line-height: 1.5;`
> - headings (`font-display`, Mitr) stay as they are.
>
> **2. Display settings helper** `src/lib/display-settings.ts` (localStorage, wrapped in try/catch like the speaking/sound settings):
> - `getThaiFont(): "traditional" | "modern"` (default `"traditional"`), `setThaiFont(v)`; setting it also sets/removes `document.documentElement.dataset.thaiFont`. Apply the saved value on app start (e.g. a `useEffect` in `RootComponent` in `__root.tsx`).
> - `getRomanMode(): "show" | "reveal"` (default `"show"`), `setRomanMode(v)`, plus a tiny `useRomanMode()` hook that stays in sync between components (a `storage`/custom event is fine).
>
> **3. `Roman` component** (`src/components/Roman.tsx`): props `{ text: string; className?: string }`. Renders nothing if `text` is empty. In `"show"` mode renders the text as today. In `"reveal"` mode renders a small ghost button "ⓘ Show sounds" (aria-label "Show transcription"); tapping it reveals the text for that word (state resets when the word changes: give it `key={word.id}` where used).
> Use it for the transcription under the Thai word in `ThaiWord` (`SessionPlayer.tsx`) and on intro screens. In the `en-to-thai` answer options and the `reading` option subtitles, **hide** the transcription entirely in `"reveal"` mode (no button inside an answer button). The wrong-answer feedback sheet always shows the transcription.
>
> **4. Quick toggle in lessons:** a small icon button in the lesson top bar (next to the hearts; use lucide `Eye` / `EyeOff`), aria-label "Show transcription" / "Hide transcription", switching between `"show"` and `"reveal"`.
>
> **5. Me page → Settings card:** two new rows in the same style as the existing ones:
> - "Thai font" with a two-option toggle **Traditional** / **Modern** (Traditional selected by default), showing a small `กขค` sample in the chosen font.
> - "Transcription" with **Always show** / **Tap to reveal**.
>
> **6. Tests:** defaults (`traditional`, `show`), setters persist; `Roman` hides text behind the button in reveal mode and shows it after a tap; renders nothing for empty text. Run the suite and confirm the build is clean.

---

## Job B: starting level on the Me page + answers fit on a laptop screen

> Two small fixes from user feedback. Keep it tight; no database changes.
>
> **1. Starting level in settings.** Learners can't find how to change their level: it's only a small "Change starting level" link on the Learn page. On `/me`, in the Settings card, add a row "Starting level" (lucide `GraduationCap`) after "Daily goal", showing the current level (Beginner / Intermediate / Advanced, or "Not set") that opens the existing `StartingLevelDialog` for the current profile (same as the Learn page's link, so the placement test is available too). The Me page is not inside `CourseGate`: if the dialog needs the loaded course, wrap it in `<CourseGate>` or render it only once the course is ready. Keep the Learn page link.
>
> **2. All answers visible on a laptop at 100% zoom.** In `SessionPlayer.tsx`:
> - multiple-choice options: `grid gap-3 sm:grid-cols-2` (two columns from `sm` up; one column on phones) and `mt-6` instead of `mt-8`;
> - `ThaiWord` Thai text: `text-[2.6rem] sm:text-[3.2rem]`, and on short screens keep it at 2.6rem (`[@media(max-height:820px)]:text-[2.6rem]`);
> - prompt block spacing: `mt-5 gap-4` instead of `mt-7 gap-5`; main area bottom padding `pb-36` instead of `pb-48` (still clear of the fixed Check bar, including the safe-area inset);
> - kids' mode keeps its larger buttons.
> Check at 1366×650 and 1280×600 viewports (typical laptop browser windows) that the prompt, all four options and the Check button are visible without scrolling, and that phones (390×700) are unchanged in layout.
>
> **3. Tests:** a render test that the options container has the two-column class; the Me page shows the Starting level row. Run the suite and confirm the build is clean.

---

## Reddit reply once live

> Thanks again for the feedback. All four are now live: Thai uses a traditional looped font by default (switch in Me → Settings → Thai font), you can set Transcription to "Tap to reveal" (or use the eye button during a lesson), Starting level is now in Me → Settings, and the answers sit in a 2×2 grid on laptops so they all fit. Let me know how it feels!
