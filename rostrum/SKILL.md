---
name: rostrum
description: "Make product films in Remotion, from storyboard to a cut that plays on a phone. Use when asked for a video, film or movie of a product, a new cut of one, or sound for it. Not for web animation (`zoetrope`) or on-screen words alone (`signage`)."
---

# Rostrum

A rostrum camera films flat artwork one frame at a time, moving slowly over it. These films work the same way: real product UI and real material, drawn frame by frame from one clock, under a camera that moves rarely.

The films are for a particular viewer (a client, a partner, a deck): usually 45 to 100 s, 1920×1080 at 30 fps, silent until sound is asked for. Other sizes when the job calls for them: the app's viewport (1440×900), 1080×1920 for a phone push, 1080×1350 for a narrated portrait cut, `--scale=2` for 4K.

## What the films get wrong

Each rule here is a correction that has already been given, often more than once.

1. **Elegant, not dense.** One idea a shot, at most three things moving, long holds. "This would overwhelm people. Should be elegant and lovely." When a cut feels busy or long, remove beats; never speed them up.
2. **Words to a minimum.** No title plate and no end plate unless asked; when asked, one very simple line in the product's mark (`M / Quote Room`). No captions unless asked. When there are captions, they are quiet, sans, visibly not part of the UI, and say what is on screen, never "us vs them". No counters, eyebrows or tracked capitals. Copy is American English, with no hedging and no em dashes; run it through `signage`.
3. **Never present it as a project.** No "Introducing", agendas, feature lists, roadmaps or framing about the film itself. Show the product doing its job. "Keep text to a total minimum and don't present it as a project."
4. **Make the case the viewer cares about.** Name the viewer and the one thing they should leave believing before anything is storyboarded. When the ask is why something works, show the principles, not a tour of features. Film the product asked for, not its neighbor: "almost like a demo of colorscope, not the demo of colorshop itself."
5. **Real product, real data.** UI comes from the product's Paper artboards, its own components or a live capture, never a lookalike: "the video looks nothing like" the Paper file. Strings, items and images come from live data; where the data has a gap, cut the beat rather than invent. Show its full range (many colors, not two) at a believable scale ("rendering it at an incorrect judged scale kills this whole thing dead"), with real names shown quietly for authenticity. Show the product at the strength it is meant to have: "31 reports reads lame." Never show scores, hex, ΔE or confidence; color is shown as color.
6. **Keep the thread.** The viewer never loses track of what is happening. Keep the subject in place and transform it rather than cutting to a new scene ("going from scene to scene we lose track of what we're doing"). Every transition shows how one state became the next; a cut whose arc can't be said in a sentence isn't ready.
7. **No jank.** Every element has a stable anchor: nothing jumps, reflows or pops when a sibling arrives or leaves. The frames either side of a continuation match exactly. "Really janky and glitchy" is the commonest complaint; fix motion before adding anything.
8. **The app is never slow.** Results land promptly and typing is quick, "snappy, but not crazy". No spinners waited out. Holds stay long enough to read.
9. **Crisp and uncropped.** Never draw an image or capture past its pixels; capture at 1.5× or more where the camera pushes in. No iframe look: no clipped panels, browser chrome or scrollbars unless the shot is about them. "Looks very soft and blurry" means the source was too small.
10. **Proud before shown.** The first thing the user sees is a finished cut, not a storyboard or a progress report, unless they asked to see one.

## The house look

- **Motion.** Arrivals ease-out quint; moves on screen ease-in-out quart; springs only for something that snaps or is thrown into place. Nothing grows from scale 0 (start at 0.94 to 0.97). Stagger siblings 2 to 10 frames. Hold at least 45 still frames before a hard cut. One slow push per hold at most, scale 1.000 to 1.015, linear. Nothing arrives while the camera moves. Transform and opacity only; no blur over large areas. Grain and a soft vignette sit over everything. For timing craft beyond this, use `zoetrope`.
- **Type.** The product's own faces, loaded from local files with `@remotion/fonts`; otherwise Inter Variable for all words and IBM Plex Mono only for literal ids and tool calls. Nothing under 20 px at 1080p. Headings Inter 500 with −0.02 to −0.035em tracking. Serif sparingly, never in form inputs. Round sizes up when a frame looks empty.
- **Color.** The product's real tokens, read from its stylesheet or Paper file.
- **Look.** Every frame should be a still worth printing: large type, generous space, real depth on materials, exact alignment. Use `chiaroscuro` for the look of reconstructed UI.

## Make the film

1. **Storyboard.** Delegate it to the strongest judgment model available as a helper when one is available, otherwise write it yourself; give it the product, the viewer, the one belief, the Paper file and access to live data. It writes STORYBOARD.md: arc, conventions, then shots in absolute frames with what is on screen, motion, exact words, data source and handoff. Before writing or briefing it, read [references/storyboard.md](references/storyboard.md) for the storyboard and build-brief templates; read each reference file with its own command. Read the storyboard critically against the rules above before building; fix it, don't relay it.
2. **Data.** Fill the storyboard's gaps from live sources into `src/data/*.json` and `public/img/`. Where data and storyboard disagree, the data wins.
3. **The frame.** Copy the kit, fonts and config from the most recent film on disk if there is one; otherwise start from [references/clock-and-kit.md](references/clock-and-kit.md), which also lists the Remotion gotchas. The lead agent owns `timeline.ts`, `Film.tsx` (one clock), `kit.tsx`, `theme.ts` and `fonts.ts`. Acts draw from the absolute frame `f` passed down; nothing in an act reads the Remotion clock.
4. **Product UI.** Before building a shot that shows the product's interface, read [references/product-ui.md](references/product-ui.md): Paper via `paste-up`, the app's own components, or a live capture.
5. **Builders.** For a film of several acts, when parallel helpers are available, write BUILD-BRIEF.md and hand each act to a helper that owns only `src/vN/act-<name>.tsx` and its parts files. Builders ask for shared-file changes in their report and never make them. Review every builder's stills yourself and send back anything ordinary. A short film is faster built alone.
6. **Look at frames.** Video can't be watched here, so look at stills. Bundle once per round (again after every edit), then run this skill's `scripts/sheet.sh` from the film's root (`$SKILL_DIR` below is this skill's folder): it renders the frames you name and tiles them into one labeled contact sheet.

   ```bash
   npx remotion bundle --out-dir=/tmp/film-bundle --log=error
   sh "$SKILL_DIR"/scripts/sheet.sh /tmp/film-bundle Agentic5 /tmp/sheet.jpg 0 180 264 410 480
   ```

   Sheet every hero frame and the last frame of every hold; before checking motion, read [references/render-and-deliver.md](references/render-and-deliver.md). Look for collisions, bad wraps, pops between consecutive frames, mismatched frames either side of a continuation, and anything soft.
7. **Cuts.** Each new cut lives in `src/vN/` with its own composition id (`Basis`, `Basis2` …) and its own `STORYBOARD-<n>.md`, opening with a section 0 of amendments when it revises an earlier one. Earlier cuts stay registered and renderable.
8. **Render and deliver.** Before rendering, read [references/render-and-deliver.md](references/render-and-deliver.md) for the settings, the phone-safe encode, GPU failures and the Stow link. A film is delivered when the user can play it on a phone from the link. Never overwrite a render that was already shared: give the new one a version suffix.
9. **Sound.** Only after the silent cut is accepted, and only when asked. Before adding sound, read [references/sound.md](references/sound.md) for ElevenLabs voices at −16 LUFS, a score that dips under them, and Kokoro for local narration.

## Report

Lead with the link or path to the film, its length and frame size. Then the frames you looked at (paths to the best stills or sheets), anything cut because the data wasn't there, and what changed since the last cut in one line each.
