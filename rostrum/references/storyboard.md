# Storyboard and build brief

Contents: what the storyboard helper gets · STORYBOARD.md template · a later cut · BUILD-BRIEF.md template.

## What the storyboard helper gets

- The product, its real functionality, and where it runs.
- The viewer and the one thing they should believe at the end.
- The Paper file or live app for the visual truth, and live data access.
- The rules from SKILL.md, the house look, and any earlier cut with what was wrong with it, quoted.
- The format, length range, and whether it is silent.
- The bar: elegant and lovely, never dense. A safe, competent board is a failure.

## STORYBOARD.md

```markdown
# <Product>, the film

1920 x 1080, 30 fps, <N> frames (<s> s). Silent. No title plate, no end plate: frame 0 is <first image>, frame <N-1> is <last image>. Built in Remotion from src/kit.tsx (composition `<Id>`).
Everything on screen comes from <data files>; no internal metric is shown.

## 1. The arc
One paragraph: what the viewer sees happen, in order, and the single thread that carries
through it (the subject that stays in place and is transformed). Say it plainly enough that
someone could retell it.

## 2. Conventions
- Colors: the product's tokens with hex, and what each is for.
- Type: faces, the four to six roles with sizes, the floor (nothing under 20 px).
- Curves: arrive, move, settle, snap, and where each is used.
- Limits: at most three things moving; holds before cuts; no pointer unless the shot needs one.
- Words: exact strings from data unless a shot says otherwise. No captions, no counters.
- Images: native sizes and the largest each may be drawn.

## 3. Shots
Frames are `start / length`, absolute and contiguous, for transcription into timeline.ts.

**01 · 0 / 120 · <Name>.**
On screen: exactly what is in frame and where (x, y, size).
Motion: what moves, when (absolute frame), curve and duration. Name the one thing the eye is on.
Words: the exact strings, or "none".
Data: the source of every value and image; the fallback if it is missing (usually: cut the beat).
Handoff: the frame where this shot is still, and what the next shot lifts or keeps from it.
Sound: where a sound would land (notes only while silent).

## 4. The moves
The film's few named moves (type a phrase, a call rises, a result settles, a flight to a slot),
each defined once with its timing, so every shot uses them identically.

## 5. Gaps
Each value the board needs but doesn't have yet, for the data pass to fill.
```

## A later cut

`STORYBOARD-<n>.md` opens with the user's verbatim note on the last cut and what the new cut changes about it, then:

```markdown
## 0. Amendments (these override the sections below)
1. **<What changes.>** Exact frames, layout and strings.
2. **Builder notes.** Composition `<Id>N`, source `src/vN/`. Don't change shared files other cuts use.
```

## BUILD-BRIEF.md

One file every builder reads. Later cuts append a section rather than replacing it.

```markdown
# Building the <Product> film: what every builder shares

Repo, Remotion version, frame size, fps, composition id. Read STORYBOARD.md in full; it is the script.
Who the film is for and what the user asked for, in their words. The bar: every frame a still you'd print.
Whether it is reconstruction or capture, and why.

## The frame you build in (read these; don't edit them)
- src/timeline.ts: SHOTS, ACTS, shared transitions, `since`.
- src/Film.tsx: one clock. Acts are FC<{f}>, drawn only inside their range, from the absolute frame.
  Never call useCurrentFrame in an act. What Film draws over the acts.
- src/kit.tsx: the curves and the film's moves, one line each.
- src/theme.ts, src/fonts.ts, src/data/*: what each holds.

You may create or edit only src/vN/act-<yours>.tsx and src/vN/act-<yours>-*.tsx parts. If a shared file
needs to change, give the exact change in your report. Others are working in the same repo. Don't commit.

## Rules
Motion, type, words and data rules from the storyboard's conventions, restated as commands,
plus the stage bounds (safe area x 120 to 1800, y 100 to 980) and any regions acts must not draw in.

## How to check your work
Bundle to your own /tmp/<you>-bundle once per round and again after edits. Render stills of your hero
frames and the last frame of every hold, and contact sheets of your motion ranges; read them.
Check frames either side of every continuation match. Iterate until each hero frame is a still you'd print.

## Report
At most 12 lines: what you built, the frames you checked with paths to your best stills,
anything you could not do, and any shared-file change you need.
```
