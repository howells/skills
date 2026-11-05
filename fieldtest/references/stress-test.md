# Stress test

The adversarial pass: feed the running app hostile, extreme and badly timed input, and report what breaks. Detect and report; layout fixes at every size belong to `reflow`.

Contents: Rules · Map the screen · Content · Behaviour · Environment · Signatures · Report

## Rules

- **Be the most awkward real user.** Name like Aleksandra Wiśniewska-Kowalczyk, a colleague at `bartholomew.fitzgerald@northwind-industries-holdings.example.com`, an intern called Jo, a workspace of 1,284 members. Apps are built against Jane Doe and twelve rows.
- **Plausible or schema-backed, never random.** Use a real naming pattern or the actual limit from the validation schema, database column or API contract. `aaaa…` at 5,000 characters proves nothing and gets dismissed. If no limit exists, that is a finding ("unbounded"); test something long but believable.
- **Enter data through the app's real boundary**: form fields, URL params, fixtures, stubbed responses. Do not edit markup or CSS to fake a break.
- **Hostile input can write before submit.** Apply the destination check in `SKILL.md` before typing, pasting, changing or blurring a field, and look for autosave and remote validation. Use a disposable target, or request interception you have verified blocks the remote write. If neither is available, skip the case and report the gap.
- **Use `example.com`, `example.org` or `.test`** for emails and URLs.
- **A predicted break is not a finding.** Report as Broken or Ugly only what rendered and misbehaved. A risk read from code or a schema without a rendered break is labelled inferred and goes under Fragile or Residual Risk.
- **Put the browser back.** Restore every setting a case changes (viewport, zoom, root font size, throttling, offline, blocked requests, emulated media, touch, direction or locale) before the next case and at the end. Report any you could not restore.

## Map the screen

Before attacking, list each value the screen renders or accepts: source, type, limit, optional or not. Include counts in headers, relative times, badge and status text, labels that come from data, tooltips, images, and the list length itself. Read limits from schemas, migrations, API types and `maxLength`. Where front end and back end disagree (50 in the form, 255 in the column), report it as Fragile.

## Content

Pick the rows that match the fields. Spread different failures across the first visible rows rather than stacking them in one.

| Field | Values to try |
| --- | --- |
| Names | `Aleksandra Wiśniewska-Kowalczyk`; `Christopher Alexander Montgomery III` (initials); `Jo`, `J`; `王秀英` (no spaces); `نور الهدى عبد الرحمن` (RTL); `Đặng Thị Ngọc Hân` (stacked diacritics); `🦊 Fox` and `👩🏽‍💻 Priya` (surrogates, ZWJ); `  Sam   Lee ` (padding); no name, only an email |
| Unbreakable strings | The long email above; `a@b.co`; a 100-character URL with a query string; a UUID; a file name like `Q3 Board Deck — FINAL (revised) v12 [approved by legal].pdf`; `Benachrichtigungseinstellungen` |
| Text blocks | Empty; whitespace only; one word; a 2,000-character pasted paragraph; a newline in a single-line field; `<script>alert(1)</script>`, `&amp;`, `**bold**` (must show literally) |
| Numbers | `0`; `1` ("1 members"); `1284`; `1000000`; `12345678.9` as currency; `-42.5`; `142%`; `0.1 + 0.2`; a count that goes `99` to `100` live |
| Collections | 0 items; 1 item; exactly page size and page size + 1; 1,000+ unpaginated; one item ten times taller than the rest; identical names |
| Time | Now ("0 seconds ago"); a future date; `1970-01-01`; late evening near a timezone boundary; a 1,284-hour duration |
| Media | A 404 avatar; no avatar; a 4000x200 panorama; a 200x4000 tall image; a transparent logo in dark mode; a slow image with no reserved space |
| Forms | Paste past `maxLength`; leading and trailing spaces; emoji and accents in fields that validate; autofill; submit with every field empty, then with one invalid |

## Behaviour

- **Rapid repeated input**: double-click and triple-click submit, hammer a toggle, press Enter twice, hold a key. Count the requests and the side effects.
- **Interruptions**: navigate away mid-submit, reload during a request, press back after a wizard step, close a dialog while it saves, open the same flow in two tabs.
- **Slow and failing network**: throttle or delay responses, then force a 500, a timeout, an empty body and malformed JSON, using the tool's request interception if available. Check the loading state, the error copy, whether retry works, and whether typed input survives.
- **Offline**: drop the connection mid-flow and restore it.
- **Order and staleness**: A then B before A resolves; see the async check in `SKILL.md`.
- **Permissions and session**: expired session mid-form, a user without access opening a deep link, the current user appearing in their own list.
- **Keyboard and focus**: tab through the stressed state; focus must not land on hidden or clipped controls.

## Environment

Run the stressed content at each of these, asserting the viewport first.

- Real container width, then 320px, then 2560px.
- Browser zoom 200% and raised root font size: text grows, boxes must not clip it.
- Dark mode, `dir="rtl"` on a wrapper where either is supported, and reduced motion.
- Touch emulation: hover-only actions are unreachable.
- Missing assets: block images, fonts and a script bundle, and see what is left.

## Signatures

| What you see | Usual cause |
| --- | --- |
| Avatar or icon squashed to an oval | Flex child shrinking; needs `flex-shrink: 0` |
| Text overflows its box | Flex or grid child with `min-width: auto` |
| Email or URL runs past the edge | No break opportunity; needs `overflow-wrap: anywhere` |
| Trailing menu or button pushed off screen | Middle content took all the space |
| Badge wraps to two lines | Badge allowed to shrink |
| Last row cut mid-glyph | Fixed height with no scroll or fade |
| Wrong initials or a replacement glyph (`�`) | Slicing code units instead of grapheme clusters |
| Orphaned dash or blank line | Placeholder rendered for a missing optional field |
| "1 members" | Hardcoded plural |
| `NaN`, `undefined`, `1284`, `0.30000000000000004` | Raw value rendered without formatting or a null guard |
| Numbers jitter as they change | Proportional figures |
| Clipped Vietnamese or Thai marks | Tight line-height with `overflow: hidden` |
| Truncated text with no way to read it | Ellipsis with no tooltip or detail view |
| Raw `<b>`, `&amp;` or `**` on screen, or script runs | Wrong escaping layer |
| Double submit creates two records | No in-flight guard or idempotency |
| Spinner never ends, or input vanishes after an error | Missing failure path |
| 1,000 rows stutter | Nothing virtualised or paginated |

## Report

Add a Stress section to the report. One row per break, worst first.

- **Broken**: content unreadable, action unreachable, wrong data shown or lost.
- **Ugly**: readable but visibly wrong.
- **Fragile**: fine today, one realistic step from breaking (no limit, no fallback).

| # | Severity | Where | Input or condition | What happened | Evidence | Likely cause |
| --- | --- | --- | --- | --- | --- | --- |

Add decisions that have more than one right answer (truncate or wrap, paginate or virtualise) with a recommendation, and list what held up so a clean result shows the attack was real. "Everything survived" with the cases tried is a complete report.
