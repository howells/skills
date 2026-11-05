# Testing on a device

Read when checking fixes. A desktop browser with a phone-sized window or device toolbar does not draw Safari's bars, safe areas or the keyboard, and has no real touch.

## What each environment shows

| Check | Desktop emulation | iOS Simulator | Real phone |
| --- | --- | --- | --- |
| Sticky hover, tap highlight | No | Partly | Yes |
| Safari status bar and toolbar, colors behind them | No | Yes | Yes |
| Safe areas, notch, home indicator | No | Yes | Yes |
| `100dvh` against moving bars | No | Yes | Yes |
| Input zoom on focus | No | Yes | Yes |
| Software keyboard layout | No | Partly | Yes |
| Touch feel, scroll physics, rubber band, performance | No | No | Yes |
| Installed-app launch | No | Yes | Yes |

The Simulator is the cheapest way to check bars, insets and viewport units. Only a phone judges touch feel and speed. Test on a phone a few years old, not the newest one.

## Reach the app

- Phone: bind the dev server to all interfaces (`--host 0.0.0.0`, or `-H 0.0.0.0` in Next.js) and open `http://<mac-lan-ip>:<port>` on the same network. A service worker needs a secure context (HTTPS or `localhost`, not a LAN IP over HTTP), so use a tunnel or the dev server's HTTPS option.
- Simulator: boot a device in Xcode's Simulator, then run `xcrun simctl openurl booted http://localhost:<port>`. The Simulator shares the Mac's localhost. If a device-control tool is available in the session, drive the Simulator through it rather than scripting `simctl` for taps and screenshots.
- Android: connect over USB with debugging on, run `adb reverse tcp:<port> tcp:<port>`, and open `localhost:<port>` in Chrome.

## Inspect

- iOS: on the phone, Settings, Safari, Advanced, Web Inspector on. In Safari on the Mac, Develop menu, pick the device or Simulator and the page.
- Android: `chrome://inspect` on the desktop.

## Pass

For each changed state, in portrait and once in landscape:

1. Tap and hold every control: no gray flash, no stuck hover, no selection or callout.
2. Focus each input: no zoom, the right keyboard, the field stays visible above it.
3. Scroll to both ends and pull past them: no refresh, no rubber-banding of a fixed shell.
4. Look at the top and bottom edges: nothing under the notch or home indicator, no band of the wrong color around the bars.
5. Open an installed copy if the app installs.

Report what you opened and on what. Anything not opened is unchecked.
