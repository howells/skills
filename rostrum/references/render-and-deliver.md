# Render and deliver

Contents: looking at motion · draft and final renders · the phone-safe file · GPU failures · delivery.

## Looking at motion

Stills show composition; motion problems show between frames. Render a range from the bundle and sheet it:

```bash
npx remotion render /tmp/film-bundle <Id> /tmp/clip.mp4 --frames=900-1080 --concurrency=6 --log=error
mkdir -p /tmp/clip
ffmpeg -v error -i /tmp/clip.mp4 -vf "select=not(mod(n\,3))" -fps_mode vfr /tmp/clip/%04d.jpg
magick montage /tmp/clip/*.jpg -tile 6x -geometry 480x270+2+2 /tmp/clip-sheet.jpg
```

Around a fast event (a burst, many items arriving), sheet every frame, not every third. For a loop, the first and last frames must be identical. Check the final MP4 too, not only the bundle: extract frames from it with ffmpeg and look at the hero frames.

## Draft and final renders

- Draft: `--scale=0.5 --crf=20 --concurrency=8 --log=error`.
- Final: `npx remotion render <Id> out/render.mp4 --codec=h264 --crf=18 --log=error`; for a final with fine type or texture, `--crf=12 --x264-preset=slow`.
- 4K from a 1080p composition: `--scale=2 --crf=16`.
- Motion blur on fast moves: render the moving layer at 8 sub-frame offsets as its own composition, average each group into `public/blur/` with a script, and draw those frames in the film. Rerun it after any change to that motion. Stacking blur samples live at render time is what loses WebGL contexts.
- Name outputs by film and version (`made-of-v3.mp4`, `basis-4-en-us.mp4`, `agentic5-silent-v2.mp4`). Before re-rendering over a file someone has seen, keep it as `-backup-<date>`.

## The phone-safe file

A film that won't play on the user's phone isn't delivered ("Can't see any video on my phone"). Remux the render with the index at the front, then check it:

```bash
ffmpeg -v error -y -i out/render.mp4 -c copy -movflags +faststart out/<film>-vN.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,profile,pix_fmt,width,height,r_frame_rate -of csv=p=0 out/<film>-vN.mp4
```

It must read `h264,…,yuv420p` with even width and height. Sound is AAC. If the file is over 100 MB (Stow's limit) or anything else is off, re-encode instead of remuxing:

```bash
ffmpeg -v error -y -i out/render.mp4 -c:v libx264 -preset slow -crf 20 -profile:v high -pix_fmt yuv420p -c:a aac -b:a 192k -movflags +faststart out/<film>-vN.mp4
```

Trim with ffmpeg only by re-encoding; a stream-copy cut freezes the first frames until the next keyframe.

## GPU failures

WebGL effects (`@remotion/effects`, light leaks, color correction, `three`) need `Config.setChromiumOpenGlRenderer('angle')`. "WebGL context was lost" mid-render comes from too many live contexts: apply one effect chain to the composite, not one per element or per blur sample. Find the cause rather than turning the GPU off: build tiny repro compositions (one per suspect, with props for count and samples) and a script that renders each and prints PASS or FAIL with the first error line, then fix until all pass.

## Delivery

1. Upload the phone-safe file with the `stow` skill and give the user the link; without it, give the local path. That is how they watch it.
2. If they asked for it in a deck or a site, use `wiredeck` or copy it to the site's public folder.
3. If the user keeps a register of finished films, add the final there with its length, frame size and source path.
