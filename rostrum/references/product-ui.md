# Product UI in a film

Three sources, in order of preference. Whichever is used, the frame must look like the product.

## 1. The app's own components

Best when the shot shows the product working. Import the app's components into the film (a bundler alias to the app's source, or a workspace package) and drive them from data: a recorded run, an event log or a JSON fixture replayed against the absolute frame. The UI is then exact, sharp at any scale, and the camera can push in freely.

- Feed props from the frame; strip the components' own CSS transitions and timers, which don't render.
- Render at the app's real viewport (often 1440 × 900), then place that viewport in the 1920 × 1080 frame, or set the composition to the viewport.
- The app's fonts and tokens come with the components; load the fonts through `@remotion/fonts` too.

## 2. Paper artboards

When the product isn't built yet, or the Paper file is the design source. Read the file through the Paper MCP (with `paste-up` when installed): exact sizes, colors and type come from the node data (JSX and computed styles), never from a screenshot. Rebuild the artboards as components in the film. When the artboards themselves are weak, improve them in Paper first, then rebuild the film from them. Paper can also hold a storyboard as a row of artboards when the user wants to see frames before motion.

## 3. Live capture

When the real behavior is the point and can't be reconstructed. The capture recipe that produced sharp footage:

- Drive a real browser by script (agent-browser or Playwriter, if available), not by hand.
- Set the window to 1.5× the layout size and zoom the page 1.5× with CSS (`html{zoom:1.5}`), holding any `100dvh` shell to the layout height, so every frame is 1.5× sharp with room for push-ins.
- Record losslessly through Chrome's screencast (CDP `Page.startScreencast` to PNG frames). Built-in browser recorders blur text.
- The screencast has no pointer. Draw the cursor or a fingertip in Remotion afterwards from the logged positions; glide it with ease-in-out and press 2 frames before the action lands.
- Wait for fonts and real content before each take; pace the script so the app is never seen waiting.
- Place footage with `<Video>` from `@remotion/media`; trim with `trimBefore`/`trimAfter`. Never scale it past its captured pixels.

## A pointer or hand

Only when the action needs one: an agent placing objects, a person choosing. It enters with purpose, travels on ease-in-out, and the target reacts on the press frame. Keyboard input is a caret and quick typing, never a visible keyboard.
