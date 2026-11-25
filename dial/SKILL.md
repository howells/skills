---
name: dial
description: "Build a dev-only /lab tool with live controls and JSON export to tune visuals, motion or a vibe. Not for UI options (`maquette`)."
---

# Dial

Prompting for an intricate visual, motion, shader or generative result is a slot machine: every round costs a full turn, lands close and gives the user no way to steer except rewriting the prompt. Build the small tool that produces the artifact instead. The process gets built once, taste decisions become live knobs the user tunes by eye in seconds, and saving exports the exact config production imports.

## Route first

Walk this before writing code:

```
Can the user point at or precisely describe the output they want?
├── Yes
│   ├── One or two direct attempts will land it, or nothing needs tuning by eye → build directly (`chiaroscuro` / `zoetrope`)
│   └── Prompting keeps missing, or taste values need live tuning → Match mode
└── No
    ├── Product UI with 3–5 discrete, nameable directions → `maquette`
    ├── Can already state the construction as rules → Explore mode, skip research
    └── Only holding a vibe (mood words, era, feeling, "I'm stuck") → Explore mode, start with research
```

**Stop-the-loop rule:** once a round of prompted attempts has been rejected ("closer, but not quite"), stop re-prompting and propose a tool. One rejected round is the proof that the user is tuning a space, not requesting a one-shot item.

## Hard rules

1. **Dev-only isolated route.** Live at `/lab/<slug>` (or the project's equivalent) and gate it out of production (`if (process.env.NODE_ENV === "production") notFound()`). Nothing in production imports from the lab route; what ships is the saved config plus the cleaned-up render logic.
2. **Rebuild the process, not the output.** Name the real technique, algorithm or medium before coding. If another app made the target, its settings panel is your parameter list. Tracing one output cannot be adjusted.
3. **Pure function of config.** One `render(config)` where `config` is a plain JSON object holding every knob (and `seed` when generative). Use a seeded PRNG (e.g. mulberry32) fed from `config.seed`, never bare `Math.random()`, so a saved config reproduces the exact frame every time.
4. **Every judgment call is a live control.** Anything you would otherwise guess or hardcode (density, timing, tension, amplitude, palette, weight, jitter) goes in the panel with tested min/max bounds so no slider reaches a broken render. Hardcode only the structural rules of the process.
5. **Instant feedback, no apply button.** Re-render live as controls move. If using a panel library (Leva, Tweakpane, custom DialKit-style drawer), keep every row unconditional; conditionally mounted rows inside folders break layout.
6. **Save writes a file.** One button persists the full current config (seed included) as pretty-printed JSON to disk via a dev-only endpoint (plus copy-to-clipboard fallback) and shows the written path. Production imports that file; never copy numbers by eye off a panel.

## Match mode (known target)

1. **Diagnose the gap.** Answer four questions from context (ask only what you cannot infer): what actually ships, why direct prompting fails, what process knows how to make it, and what format production needs (performance, interactivity, file size). Classify the gap (most tools combine two):
   - **Dial-in**: depends on eye-judged values → bind every taste parameter to a live control.
   - **Matching**: must match an existing visual or app output → render live output beside the target image at the same pixel size.
   - **Converter**: right pixels or data, wrong format → ingest source, export the exact format production needs.
   - **Stage**: can only be judged in a hard-to-reach state → route that puts the work in that state immediately.
2. **Pitch in four lines** before coding: **The gap**, **The tool** (branch + what it renders), **The controls**, **The export** (format + save path). If the user is waiting, pause a beat to let them redirect; if they already said go, state the pitch and build.

## Explore mode (only a vibe)

1. **Research the visual language.** Keep the user's vibe words verbatim. Investigate the physical or historical tradition behind them to answer: what process made this look (medium, printing method, tool, era), what constraints it imposed on colour, texture and composition, and what its recurring motifs are called. Compress into 5–10 concrete constraints plus named motifs, and show them to the user to strike or keep before any code exists.
2. **Sort into three buckets** and state them in a few lines:
   - **Rules** — what makes it this idea; hardcoded.
   - **Modes** — discrete sub-directions or motifs; tabs or select.
   - **Knobs** — every continuous taste value; live controls with tested bounds.
   If the knob bucket is empty, build the output directly.
3. **Make variation free.** Render one large canvas at real size (not thumbnails), display the current seed, click the canvas for a fresh random seed, and include a rail of saved configs that re-applies any keeper on click so the user can compare by eye.

## Build and hand off

Build the tool in one sitting with no ceremony; it is scaffolding, not a product. In Match mode, keep the target visible beside the live output at shipping size. Hand off in two lines — the URL and the verbs (*tweak knobs, click canvas for a new seed, save to keep*) — then stop and let the user dial it in.

## Harvest

When the user picks a saved keeper:

1. Read the saved JSON file from disk; never eyeball values from a screenshot.
2. Wire the saved config and cleaned-up render logic (or static SVG/PNG export) into the real production location.
3. Leave `/lab/<slug>` in place unless asked to delete it so future assets in the same visual language reuse the tool, and confirm it remains gated out of production.

## Invocation variants

| Invocation | Behaviour |
| --- | --- |
| `<thing or vibe>` | Full flow: route → diagnose or research → pitch → build → hand off |
| `diagnose` | Diagnose the gap and pitch the tool; build nothing |
| `research <vibe>` | Return constraints and named motifs; build nothing |
| `harvest` / `harvest <path>` | Wire the latest or named saved JSON config into production |
| `more knobs` | Promote hardcoded values in the current tool to live controls |
| `new mode <description>` | Add a discrete sub-direction to the current tool |
