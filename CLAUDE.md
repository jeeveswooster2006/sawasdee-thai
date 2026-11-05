# Rules for this project (Nong Chang & Family)

## Pictures and videos
- **Every animal must have the correct number of limbs for its species.** Elephants, bulls and other four-legged animals have exactly four legs and no hands or arms; birds have two legs and two wings; people have two arms and two legs. No extra, missing, merged or duplicated limbs.
- **What counts as a failure (Paul, 31 Oct 2026):** extra or missing limbs, or limbs merging into other objects. An animal using its legs or wings like arms (holding a book, waving, standing upright) is fine as long as it still has the right number of limbs — don't flag or redo pictures for that.
- Write this into every image or video prompt (ComfyUI, Gemini or any other tool), and check every generated picture or clip for it before using it. Redo anything that fails.
- The ComfyUI scripts add it automatically (`ANATOMY` in `tools/art/generate_unit_art_comfyui.py`, also used by `tools/video/generate_clips_comfyui.py`).

## Use cheaper models where they're good enough (Paul's request, 28 Oct 2026)
Hand work to a Sonnet or Haiku subagent (Agent tool with `model: "sonnet"` or `"haiku"`) whenever it doesn't need the main model's judgement. Give the subagent a complete, standalone brief: it starts with no context.
- **Haiku:** mechanical, step-by-step jobs, such as:
  - recording audio batches (generate, poll, download, split with `fetch_split.sh`, check the clip count);
  - polling a running Lovable message or ElevenLabs job;
  - file and format checks;
  - git housekeeping.
- **Sonnet:** content and checking work, such as:
  - drafting or proofreading lesson word lists and translations;
  - social captions and tags;
  - summarising Lovable code files;
  - content audits (missing audio, duplicate answers, emoji give-aways).
- **Keep in the main model:**
  - writing Lovable briefs and reviewing Lovable diffs for safety;
  - estimating and spending credits;
  - anything that publishes;
  - final checks of pictures and videos (the limb rule);
  - talking to Paul.

Don't delegate tiny tasks: a subagent costs a fresh start, so it only pays off for jobs of a few minutes or more.

## App code lives on GitHub now (since 30 Oct 2026)
The Lovable app is two-way synced with **jeeveswooster2006/sawasdee-family** (branch `main`).
- Make code changes there directly. Pushing to `main` updates Lovable's editor and preview within about a minute and costs no Lovable credits. Run `npx tsc --noEmit` and `npx vitest run` first.
  - The lockfile points at Lovable's private registry, so install with `npm install --no-package-lock --legacy-peer-deps --ignore-scripts --registry=https://registry.npmjs.org`, then `npm install --no-save @testing-library/dom`.
- Live only changes when Paul says "publish": then deploy with the Lovable tool (free).
- Database migrations or Lovable-only features (email, auth providers, secrets) may still need a Lovable message. Check first.

## Working with Paul (standing rules)
- Never publish anything (app deploy, moving `live.json`, or a live database change that isn't fixing something broken) until Paul says "publish".
- Never ask for or accept passwords, API keys or other credentials. Paul types secrets into the service himself.
- Paul uses a phone and prefers short, simple messages with explicit tap-by-tap steps. Lead with the outcome.
- Before spending Lovable credits, say the realistic cost first: actual cost runs 2–3× the gut estimate. Paul gets 5 credits a day. Prefer free GitHub changes.
- Lovable also edits the app (security scans etc.). Before publishing, review any new Lovable commits and migrations on `sawasdee-family` main: on 1 Nov a Lovable security fix revoked direct writes while the app still used them, and rejected Thai word ids.
- Pictures: only extra/missing limbs or limbs merging into objects count as failures (see the top of this file).
- The live database is Lovable Cloud project `e31b84f7-44c3-4a30-92e8-dc156d90824d`; check and change it with the Lovable `query_database` tool.
- Start new Claude Code sessions from `jeeveswooster2006/sawasdee-family` (app) and add this repo; the old `which-pet-shines` repo is unrelated and may be deleted.

## Parked ideas (Paul, 1 Nov 2026)
Not started. Only pick these up when Paul asks.
- Maybe move the domain (nongchang.co.uk) and email to Cloudflare or Proton. Left for now.
- Maybe upgrade ElevenLabs to the Creator plan when a fourth language is built.
- A "Sounds of French" / "Sounds of Spanish" track in the app, like Read Thai.
- Facebook posts that Paul publishes himself.

## Email (set up 2 Nov 2026)
- News emails go through **Resend** (Claude connector) from `Nong Chang & Family <hello@news.nongchang.co.uk>`, replies to `info@nongchang.co.uk` (Fasthosts mailbox). Domain `news.nongchang.co.uk` is verified (EU region, no open/click tracking).
- DNS is at **Cloudflare**; the Cloudflare connector can edit records. Root mail (MX/SPF) stays with Fasthosts; don't touch it.
- App opt-in: "News emails" tick box at sign-up and switch in Me & settings (`news_emails` in user metadata). Before each send, copy only opted-in accounts to Resend; Resend handles unsubscribes.
- Sent so far: 2 Nov "sorry you couldn't get in" (one-off account help, 7 unconfirmed sign-ups) and "While you were away" broadcast to 26 existing users (segment "App users (Nov 2026)"). Future news emails go to opted-in users only.
- Paul approves every email ("send") before it goes out; send a test to info@ first. Hotmail/Outlook currently files our mail in Junk (new sender); Gmail delivers to Important. Keep subjects plain, no emoji.

## Facebook page (set up 4 Nov 2026)
- Page "Nong Chang" (Education) and Instagram **@nong_chang26** (Professional, linked to the page). Posts are scheduled through the **Metricool** connector (brand id 7865277, free plan: 20 posts/month). Instagram is connected with an Instagram login (connecting via Facebook didn't pick up the account).
- Paul approves every batch with "post" before anything is scheduled. Keep personal details out: "a dad in the UK" is the only personal line.
- Pictures and post texts live in `social/facebook/` (cards are made with the brand fonts Mitr/Sarabun; `nov-2026-posts.json` holds the November plan). Images are served from jsDelivr at the commit they were added in.
- November 2026: 16 posts scheduled to both Facebook and Instagram, weekdays 7pm UK, 5–26 Nov (4 spare). Metricool accepted all 16 on both networks, so one post to both seems to count once; check after the first ones publish. Instagram captions can't hold links, so the profile link matters. Weekly pattern: Mon Thai word, Tue French/Spanish word, Wed Read Thai letter, Thu family tip/question, Fri fun fact. Language content is proofread by a Sonnet subagent before scheduling.

## Weekly family email (live 5 Nov 2026)
- Goes out Sundays 18:00 London to opted-in adult account owners only (code: `src/lib/weekly-email*.ts` in sawasdee-family). Database timer: Lovable-managed pg_cron jobs `weekly-family-email-utc17` and `-utc18` POST to /api/public/weekly-email with the cron secret (set up by Lovable 5 Nov); the route ignores calls outside the window, and a family gets at most one per week.
- Needs the `RESEND_API_KEY` secret in Lovable (Paul adds it himself).
- When something important ships (e.g. a new language), add a line to `src/lib/whats-new.ts` so it appears in that week's email.

## App roadmap (Paul, 5 Nov 2026)
Build in this order. Each one is free on GitHub, shown in the preview, and only published when Paul says "publish".
- **Now (top three, built 5 Nov, in preview):** 1 Family goal (shared weekly points jar, reward on Sunday, in the weekly email) · 10 Share cards ("Mia learned 50 Thai words!" picture to share, with app link) · 5 Picture stories (short illustrated stories with native voices using learned words; limb rule applies to art).
- **Then one a week, released on Fridays so the app visibly improves each week (scheduled tasks build it that day; Paul still says "publish"):** 14 Nov evening: 2 Play together (pass-the-phone quiz) · 21 Nov afternoon: 4 Kids teach the grown-ups · 28 Nov evening: 6 Look after Nong Chang (feed/outfits), **kids' mode only** · 5 Dec afternoon: 7 Install as an app + daily reminder · 12 Dec evening: 9 Printables (flashcards, fridge words, colouring sheets). Build each one only on its Friday, so a publish never ships next week's feature early.
- **Back burner, reminder 5 Jan 2027:** 8 Holiday packs · 11 Invite a family · 12 Schools and clubs.
- **No:** grandparent link.
- Mark items done here as they ship.
