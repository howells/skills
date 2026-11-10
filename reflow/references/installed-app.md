# Installed app meta

A tab in Safari and an installed copy are different environments: standalone mode has no address bar or toolbar, so viewport, safe areas and status bar all change.

On iOS 26 any site can be added to the Home Screen, and it opens as a web app by default; the user can turn off Open as Web App to get a plain bookmark. Keep `display: standalone` in the manifest, and check the launch mode the installed copy actually gets.

## Manifest

```json
{
  "name": "Product name",
  "short_name": "Product",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#ffffff",
  "icons": [
    { "src": "/apple-touch-icon.png", "sizes": "180x180", "type": "image/png" },
    { "src": "/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ]
}
```

Link it with `<link rel="manifest" href="/manifest.webmanifest">`. `background_color` is the launch splash; `theme_color` tints the installed window's title bar on Android. Both should be the color at the very top of the page. In Next.js use `app/manifest.ts` and the `viewport` and `metadata.appleWebApp` exports instead of hand-written tags.

## iOS tags

```html
<meta name="apple-mobile-web-app-title" content="Product">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<link rel="apple-touch-icon" href="/apple-touch-icon.png"> <!-- 180x180, opaque, no rounded corners -->
```

- The manifest's `display: standalone` sets the launch mode; `apple-mobile-web-app-capable` adds nothing beside it.
- `status-bar-style`: `default` is dark text on a light bar; `black-translucent` lets the page paint under the status bar, which needs `viewport-fit=cover` and top-inset padding; `black` is a solid black bar.
- Which source iOS uses for the home-screen icon has changed between versions, so list the 180×180 icon in both the manifest and the apple-touch-icon link. Give it an opaque background and square corners; the platform applies the corner mask.

## Traps

- Service workers need a secure context: HTTPS or `localhost`, not a LAN IP over HTTP. Use a tunnel or the dev server's HTTPS option when testing on a phone.
- In standalone mode there is no back button. Every screen needs its own way back.
- Links outside the manifest `scope` open in a browser view. Keep navigation inside scope.
- Pull-to-refresh and the rubber band are the main giveaways in standalone mode, so set `overscroll-behavior` (the baseline in SKILL.md).
- Cached manifests and icons stick. Remove the installed copy and add it again after changing them.

## Check

Install a copy on a device or in the Simulator (Share, then Add to Home Screen). Launch it from the icon, confirm it opened as a web app rather than in Safari, then check the splash, status bar, safe areas, back navigation and a cold start with no network if a service worker is meant to serve it.
