# Sound

Sound goes on a picture that has already been accepted silent. Where voices drive the timing, the picture is re-timed to them, never the voices squeezed to the picture.

## Voices with ElevenLabs

Script the lines in a typed module (`src/lines.ts`: speaker, text, the frame it should start near), then generate them with a script that writes one file per line and a timing JSON the film reads. Key from `ELEVENLABS_API_KEY`, passed with `node --env-file`; fail loudly without it.

- Endpoint: `POST /v1/text-to-speech/{voice_id}/with-timestamps`, `output_format=mp3_44100_128`, `model_id` the current top model (check the models endpoint). Character timings come back with the audio; turn them into word start times for the timing JSON, which drives anything on screen that follows the voice.
- Pass `previous_text` and `next_text` with each line, so the delivery runs on from line to line. Without them each sentence starts cold.
- Voice settings near `stability 0.45–0.5`, `similarity_boost 0.75–0.8`.
- Level every take to −16 LUFS so no voice sits under another:
  `ffmpeg -i in.mp3 -af loudnorm=I=-16:TP=-1.5:LRA=7 -ar 44100 -b:a 128k out.mp3`
- Add a `--reuse` flag that keeps takes on disk and only re-levels them; regenerating costs credits.
- Place each line with `<Sequence from={at}><Audio src={staticFile(file)} /></Sequence>`, `Audio` from `@remotion/media`. Leave about 14 frames between lines and 24 before the first.

## Local narration with Kokoro

For a narrated cut that doesn't need a cloned voice, or when there's no key. `kokoro-onnx` with the v1.0 model files cached in `~/.cache/kokoro`; run the script with `uv run` and inline dependencies. Speed around 0.94; pick a voice that matches the copy's English. Write each sentence to its own file, level it (`loudnorm=I=-18:TP=-1.5:LRA=7`), measure it with ffprobe, and write a narration JSON of chapters and segments in frames. The film's duration and shot lengths come from that JSON.

## Music

Keep it calm, never cute.

1. Build a click track from the edit: 120 BPM at 30 fps is 15 frames a beat, 60 a bar. Put the film's moves on bar lines; the edit should already respect them.
2. Synthesize a guide from the cue sheet (builds, drops, hits) and dip it under the voices, then mux a guide preview so the user can judge the shape before paying for music.
3. Generate with ElevenLabs Music (direct, or `fal-ai/elevenlabs/music` on fal), one chunk per move, each cut to the bar and between 3 and 120 s, with the same positive and negative styles throughout so the chunks join.
4. Dip the score 15 dB under the voices: from half a second before the first word to half a second after the last, on 0.45 s cosine ramps. Score sits around −20 LUFS against voices at −16.
5. A fully synthesized score (oscillators and noise rendered by a script) suits a quirky sizzle with no voices.

## Mix and check

Render the voices alone to a WAV (`--codec=wav` with a prop that mutes the score) to lay trial scores under. Render the final with sound, then measure the whole film: `ffmpeg -i film.mp4 -af loudnorm=print_format=summary -f null -`. Integrated loudness near −16 LUFS, true peak below −1 dB. Listen-checks aren't possible here, so read the levels and look at word timings against the picture; say what you couldn't hear.
