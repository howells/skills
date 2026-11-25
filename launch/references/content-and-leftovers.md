# Lane H — Content & leftovers

Catches unfinished copy, fabricated proof, exposed dev tools and secret leaks. Deep fixes belong to `typecase` (fonts), `signage` (UI copy) and `unslop` (code tells). Never invent real copy or proof; flag missing content on the human list.

## Content

- **H1. No placeholder content (BLOCKER on public pages)** — Hunt (case-insensitive): `lorem|ipsum`, `John Doe|Jane Doe|Acme`, `example\.com|test@|foo@bar`, `TODO|TBD|coming soon|WIP`, `Untitled|My App|Create Next App|Vite \+ React`, `via\.placeholder|placehold\.co|picsum`, `href="#"`, `href=""`, default framework favicon, filename `alt` text. Vet seeded docs examples.
- **H2. No fabricated social proof (BLOCKER)** — Hunt: testimonials, user counts ("10,000+ teams"), logo walls, uptime/compliance badges ("SOC 2", "99.9%") with no human source or data file in the repo. Never reword fake proof — remove or flag for the user to confirm.
- **H3. Specific buttons, links and errors (SHOULD FIX)** — Hunt: `Submit`, `OK`, `Click here`, `Learn more`, `Something went wrong`, `Invalid input`. Fix when the action is obvious from the handler (`Save changes`, `Create project`); otherwise flag (`signage`).
- **H4. Missing font weights fail visibly (SHOULD FIX)** — Hunt: CSS `font-weight` or `italic` values not loaded in `@font-face` / `next/font`; missing `font-synthesis: none`. Add `font-synthesis: none` and list unloaded weights (`typecase`).
- **H5. Line breaks and measure (POLISH)** — `text-wrap: balance` on `h1`–`h3`, `text-wrap: pretty` on `p`, reading measure capped near `65ch`.
- **H6. Real typographic characters (POLISH)** — Hunt: `...` in rendered UI copy (`Loading...` → `Loading…`), straight quotes in marketing copy. Leave code, keys and logs untouched.
- **H7. Casing lives in CSS, not raw caps (POLISH)** — Replace raw ALL-CAPS text in markup with sentence case (remember `chiaroscuro`'s rule against tracked uppercase labels).
- **H8. Locale declared (SHOULD FIX)** — `<html lang="…">` present; use `Intl.DateTimeFormat` / `Intl.NumberFormat` where multi-locale formatting applies.

## Leftovers

- **H9. Dev tools gated out of production (BLOCKER)** — Hunt: `DirectionPicker` (`maquette`), `leva` / `useControls`, `tweakpane`, `ReactQueryDevtools`, `react-scan`, `eruda`, debug/feature-flag overlays. Gate behind `NODE_ENV === "development"` (or `import.meta.env.DEV`) with dynamic import so bytes stay out of production. Confirm values dialled in with `dial` come from a saved JSON config, not a hidden panel default.
- **H10. Scaffolding routes gated out of production (BLOCKER)** — Hunt: `/lab/*`, `/proto/*`, `/test`, `/playground`, `/sandbox`, `/debug`, `/styleguide`, or sitemap entries pointing to them. Gate with `if (process.env.NODE_ENV === "production") notFound()` and disallow in `robots`; never delete `/lab/*` unasked (`dial` keeps tools on purpose), list them for the user to decide.
- **H11. No stray debug output (BLOCKER if logging user/auth/payment data, SHOULD FIX otherwise)** — Hunt: `console.log`, `console.debug`, `console.table`, `debugger`, `alert(`, `<pre>{JSON.stringify(...)}</pre>`. Keep deliberate `console.error` in error boundaries or loggers.
- **H12. No secrets or dev URLs in client code (BLOCKER — report above the verdict)** — Hunt: `localhost`, `127.0.0.1`, `ngrok` in source; `NEXT_PUBLIC_*` / `VITE_*` / `PUBLIC_*` containing `SECRET`, `PRIVATE`, `SERVICE_ROLE`; key-shaped literals (`sk_live_`, `sk_test_`, `eyJ…`); tracked `.env` files. Name the file and variable only, never the value, and flag key rotation as urgent.
- **H13. Commented-out code and risky markers (SHOULD FIX)** — Hunt: commented-out blocks (delete), `.only(`/`.skip(` in tests, `V2`/`Copy`/`Temp` files, recent `@ts-ignore`/`as any`, and `TODO`/`FIXME` on auth, permissions, billing or deletion paths (report those verbatim).
- **H14. Diff tells & generated visuals (POLISH)** — Note leftover agent tells (`unslop`) or obvious generated-looking marketing clichés (`chiaroscuro`) in one line for after launch; flag emoji used as functional UI icons as SHOULD FIX.
- **H15. Human check (always)** — Put on human list: read every word of landing, pricing and signup pages; click every header and footer link; verify every number, logo and quote is real.
