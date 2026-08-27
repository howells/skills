# Interface: Performance

Performance is part of finish: input should acknowledge immediately, content should not jump, and the interface should remain usable while work is pending. Measure the real route before prescribing a fix.

## Establish the Problem

- Reproduce with representative data and the actual device or browser class at risk.
- Separate network latency, server work, JavaScript execution, rendering, image cost, and animation cost.
- Record the visible symptom and a measurement before optimizing.
- Disable extensions or development instrumentation when they distort the result, but keep a normal development pass for framework warnings and rerenders.

Do not adopt fixed latency budgets or a virtualization library without product context. The useful threshold is the one at which this task loses continuity or blocks input.

## Stable Rendering

- Reserve intrinsic space for images, media, async controls, validation, and loading content.
- Keep button width and labels stable while submitting; expose pending state with `aria-busy` where appropriate.
- Match skeleton geometry to final content and avoid indefinite shimmer as decoration.
- Use tabular figures where changing numbers would shift adjacent content.
- Preserve focus and user input through hydration and async updates.
- Prevent a flash of the wrong theme or persisted state with server-provided state, an early bootstrap, or CSS that does not hide usable content indefinitely.

Persist only state that should survive. Do not put every tab, accordion, or toggle in storage by default; decide whether it belongs in the URL, server state, local storage, session storage, or nowhere.

## Layout and Rendering Work

- Batch related DOM reads before writes when imperative code is unavoidable.
- Avoid work proportional to the whole document for a local interaction.
- Virtualize only when rendering the actual collection is measurably costly and accessibility, search, print, and variable-height behavior remain sound.
- `content-visibility: auto` can defer off-screen rendering for suitable long sections; provide a realistic `contain-intrinsic-size` and test scroll anchoring.
- Large blurs, filters, shadows, masks, and many promoted layers can be expensive. Remove unearned effects first, then measure retained ones.
- Use `will-change` narrowly and temporarily when evidence shows it helps. Layer promotion consumes memory and is not a general performance switch.

CSS custom properties are not inherently slow. The cost depends on inheritance, invalidation scope, the consuming property, and update frequency. Avoid high-frequency updates to inherited variables across large subtrees; register non-inheriting typed properties or scope variables locally when that reduces measured work.

## Images and Media

- Give images intrinsic dimensions or an aspect ratio.
- Prioritize the actual largest-content image; lazy-load content that begins off screen.
- Serve appropriate formats, resolutions, and responsive sources.
- Pause or unmount off-screen video when continuing playback serves no user purpose.
- Autoplaying inline video needs `muted` and `playsinline`, a poster, and a reduced-motion or user-control strategy.

## Motion

Prefer properties and implementation paths that meet the visual need with stable frame times, but do not repeat categorical compositor or main-thread claims across browsers and library versions. Profile the chosen implementation.

- CSS is often sufficient for local deterministic transitions.
- Web Animations or a library may help with interruption, gesture input, exit presence, or orchestration.
- `transform` and `opacity` are useful defaults for spatial and visibility changes, not a guarantee of zero paint or memory cost.
- Theme changes usually should not animate every descendant. Limit transitions to intentional surfaces or temporarily suppress only the transitions that create a visible flash.

See [animation.md](animation.md) for the motion contract.

## Perceived Speed

- Acknowledge input immediately.
- Keep the user's context visible during work.
- Show determinate progress when the system can estimate it honestly.
- Use optimistic updates only when failure can be reversed and pending state remains clear.
- Stream or reveal meaningful partial results when they are independently useful; do not animate placeholders to disguise avoidable delay.

## Verify

Exercise the complete path with representative data, slow network or CPU where relevant, keyboard and pointer input, background-tab return, mobile viewport, and reduced motion. Check console and network errors alongside responsiveness, layout shift, memory growth, and whether the user's action reaches its downstream effect.
