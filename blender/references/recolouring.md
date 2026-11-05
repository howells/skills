# Recolouring from render passes

Compositor names below are Blender 5.x; check the installed node and property schema before using them on 4.x.

Decompose because paint applied to an 8-bit render multiplies onto clipped pixels: the sunlit wall is already white and there is nothing left to tint. Everything before the tone map stays float.

## The identity

Cycles composes a diffuse material as

```
combined = diffuse_colour × (diffuse_direct + diffuse_indirect) + rest
```

The lighting terms are already divided by the diffuse colour, so swapping paint replaces a factor:

```
out = mix(albedo, paint, mask) × light + rest
```

Prove the wiring first: recolour back to the grey the scene was rendered with and difference against the beauty pass. Mean relative error around 2.5e-4 (half-float storage) is right; larger means the passes are wired wrong.

## Two methods

| | renders | gets right | gets wrong |
|---|---|---|---|
| **passes** | 1 | the painted material's own reflectance, exactly | light bounced off it still carries the traced grey, so bright paint comes out too dark |
| **basis** | 4 (black + unit R, G, B) | first-order inter-reflection, including light the painted material bounces back onto itself | second-order bounces |

Basis: `L(c) = L(0) + c_r(L(R) − L(0)) + c_g(L(G) − L(0)) + c_b(L(B) − L(0))`. It is first-order in the painted albedo, so not exact for multi-bounce transport; compare against a traced rerender when accuracy matters. In the shader it is three multiply-adds.

## Scoring

- **Not per-pixel relative error.** It divides by near-zero in every shadowed corner; scored that way the better method looked three times worse. Use absolute luminance error against the region's mean luminance.
- **Refuse on a resolution mismatch.** A 420×280 basis against 480×320 passes compares unrelated pixels and returns a plausible 52.8% where the truth was a few percent. It doesn't error.
- **p90/p10 is not a contrast measure.** It is near scale-invariant and barely moves.
- **A gate measuring what a region claims is blind to a region claiming nothing.** Skipping regions under 100 px is reasonable, but then a cornice reduced to 0 px passes. Keep both: a `SURVIVES` check for a declared region reduced to nothing, and an `unclaimed` mask for pixels no material declared.
- **Prove the image could show the defect.** A boundary fault is invisible when both sides are close in tone, and harmonious schemes hide exactly that. Assert the median luminance separation of adjacent regions and refuse below a threshold.

## Getting passes out

- Render layer sockets are spelled in full: `"Diffuse Direct"`, not `"DiffDir"`.
- Multilayer EXR is gated behind `image_settings.media_type`.
- `ID Mask` takes its index on an input socket. Object pass indices → `ID Mask` → RGBA coverage mattes, four regions per texture.
- File Output uses `directory` plus `file_output_items.new(type, name)`.
- The compositor tree is `scene.compositing_node_group`.
- For a basis, hold seed and sampling constant across the four renders and turn denoising off; denoiser bias becomes a fixed offset in the difference.
- Write `Linear Rec.709`, view transform `Standard`, look `None`, exposure 0.

## Into a browser

Browsers can't read EXR and an 8-bit intermediate clips the highlights this exists to keep. Pack half-float, gzip the raw `.f16`, decompress with `DecompressionStream("gzip")`, and upload straight to WebGL2:

```js
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA16F, w, h, 0, gl.RGBA, gl.HALF_FLOAT, new Uint16Array(bytes));
gl.getExtension("OES_texture_float_linear");  // without it every filtered sampler returns black
```

Blender returns rows bottom-up. If the packer flips them, the shader must not flip `v`, and vice versa. A stale pack with only one side changed stands the room on its ceiling.
