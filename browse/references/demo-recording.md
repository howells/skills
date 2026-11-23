# Demo recording

A demo is a short video of a real flow that a viewer can follow: a pointer gliding to each control, a pulse on each click, no dead air. The finished file is an MP4 at the page's CSS size.

## 1. Tab

Open the tab with `keepVisible: true` and an `allowedOrigins` list. Without `keepVisible` the tab sits in the background, Chrome freezes its animations, and every pointer move lands in one jump.

Set the size once: `await page.setViewportSize({ width: 1440, height: 900 })`.

Rehearse the whole flow unrecorded first, then put the page back to its starting state before the take.

## 2. Cursor

The recorder (CDP screencast) captures no pointer, and browse's human-like input sends its own mouse paths. So draw the pointer in the page, animate it with a CSS transition (runs on the compositor, smooth whatever the relay latency), and let it follow real pointer events only during a drag.

Re-run `install()` after every navigation; the overlay lives in the page.

```js
const CURSOR = `(()=>{if(window.__cursor)return;
const el=document.createElement('div');
el.innerHTML='<svg width="26" height="26" viewBox="0 0 28 28" style="display:block"><path d="M8.2 4.9v16l3.7-3.6 2.4 5.8 2.8-1.2-2.4-5.6h5.2z" fill="#fff"/><path d="M9.2 7.3v11.3l2.9-2.8.4-.1 2.3 5.4 1-.4-2.3-5.4h4z" fill="#000"/></svg>';
Object.assign(el.style,{position:'fixed',left:'-8px',top:'-4px',zIndex:2147483647,pointerEvents:'none',willChange:'transform',filter:'drop-shadow(0 1px 1.5px rgba(0,0,0,.35))'});
const ring=document.createElement('div');
Object.assign(ring.style,{position:'fixed',left:'-14px',top:'-14px',width:'28px',height:'28px',borderRadius:'50%',background:'rgba(0,0,0,.18)',zIndex:2147483646,pointerEvents:'none',opacity:'0'});
document.documentElement.append(ring,el);
let x=innerWidth/2,y=innerHeight/2,tracking=false;
const put=ms=>{el.style.transition=ms?'transform '+ms+'ms cubic-bezier(.45,0,.2,1)':'none';el.style.transform='translate('+x+'px,'+y+'px)'};put(0);
const onMove=e=>{if(tracking){x=e.clientX;y=e.clientY;put(0);}};
addEventListener('pointermove',onMove,true);addEventListener('dragover',onMove,true);
window.__cursor={
 at(nx,ny){x=nx;y=ny;put(0);},
 track(on){tracking=on;},
 moveTo(tx,ty,ms){x=tx;y=ty;put(ms);return new Promise(r=>setTimeout(r,ms+30));},
 click(){ring.style.transition='none';ring.style.opacity='1';ring.style.transform='translate('+x+'px,'+y+'px) scale(.4)';ring.getBoundingClientRect();
  ring.style.transition='transform 380ms cubic-bezier(.2,.7,.3,1),opacity 380ms ease-out';ring.style.transform='translate('+x+'px,'+y+'px) scale(1.3)';ring.style.opacity='0';}
};})()`;
let pos = [720, 450];
const install = async () => {
  await page.evaluate(CURSOR);
  await page.evaluate(([a, b]) => window.__cursor.at(a, b), pos);
};
// One real move per glide: the overlay animates, the page still gets hover.
const glide = async (x, y, ms = 650) => {
  await page.evaluate(
    ([a, b, m]) => window.__cursor.moveTo(a, b, m),
    [x, y, ms]
  );
  await page.mouse.move(x, y);
  pos = [x, y];
};
const clickFx = () => page.evaluate(() => window.__cursor.click());
const center = async (loc) => {
  const b = await loc.boundingBox();
  return [b.x + b.width / 2, b.y + b.height / 2];
};

// A click: glide, pulse, then the real click.
//   await glide(x, y); await clickFx(); await locator.click();
// A drag: the overlay follows the real pointer for its duration.
//   await page.evaluate(() => window.__cursor.track(true));
//   await browse.drag({ from: { x: x1, y: y1 }, to: { x: x2, y: y2 }, steps: 30 });
//   await page.evaluate(([a, b]) => { window.__cursor.track(false); window.__cursor.at(a, b); }, [x2, y2]);
```

## 3. Take

Run the whole take in one `execute` with a long `timeoutMs`, between `browse.recording({ action: 'start', path: 'name.mkv', frameRate: 30 })` and `browse.recording({ action: 'stop' })`. Record to `.mkv`: it writes device-resolution frames directly, and the encode step below handles the frame sizes.

Pace for a viewer: glides of 500–900 ms, a beat of 250–400 ms before each click, 2–4 s holds on anything worth reading. End on the screen that proves the point; a third-party page reached at the end can greet the viewer with region or cookie pop-ups.

## 4. Encode and check

With an emulated viewport, most frames carry the page in their top-left corner with blank margins, and a few come at the exact page size. Crop every frame to the viewport at device scale (1440×900 at 2× is 2880×1800), pad, then scale:

```bash
ffmpeg -y -i take.mkv \
  -vf "crop='min(iw,2880)':'min(ih,1800)':0:0,pad=2880:1800:0:0:white,scale=1440:900:flags=lanczos,fps=30,format=yuv420p" \
  -c:v libx264 -crf 18 -preset slow -movflags +faststart -an demo.mp4
```

Done means you have looked at frames from the MP4: a contact sheet of the whole take, and one glide at 10 fps showing the pointer advancing frame by frame. Then delete the `.mkv` (hundreds of MB) and put the page back to its starting state.
