#!/bin/sh
# sheet.sh <bundle-dir> <composition> <out.jpg> <frame> [frame ...]
# Renders a still of each frame from a Remotion bundle, in parallel, and tiles
# them two across into one contact sheet labeled by frame number.
# Run from the film's root, where `npx remotion` resolves.
set -u

if [ $# -lt 4 ]; then
  echo "usage: sheet.sh <bundle-dir> <composition> <out.jpg> <frame> [frame ...]" >&2
  exit 2
fi
bundle=$1 comp=$2 out=$3
shift 3

[ -f "$bundle/index.html" ] || { echo "sheet.sh: $bundle is not a Remotion bundle; run npx remotion bundle --out-dir=$bundle first" >&2; exit 1; }
command -v magick >/dev/null 2>&1 || { echo "sheet.sh: ImageMagick 7 (magick) is not on PATH; brew install imagemagick" >&2; exit 1; }

dir=$(mktemp -d "${TMPDIR:-/tmp}/sheet.XXXXXX")
for f in "$@"; do
  npx remotion still "$bundle" "$comp" "$dir/f$f.jpg" --frame="$f" --log=error > "$dir/f$f.log" 2>&1 &
done
wait

failed=0
for f in "$@"; do
  if [ ! -s "$dir/f$f.jpg" ]; then
    echo "sheet.sh: frame $f did not render: $(grep -m1 'Error:' "$dir/f$f.log" | sed 's/^ *Error *//' | cut -c1-200) (log: $dir/f$f.log)" >&2
    failed=1
  fi
done
[ $failed -eq 0 ] || exit 1

set --
for f in $(ls "$dir"/f*.jpg | sed 's/.*\/f\([0-9]*\)\.jpg/\1/' | sort -n); do
  set -- "$@" -label "$f" "$dir/f$f.jpg"
done
font=/System/Library/Fonts/Helvetica.ttc
[ -f "$font" ] && set -- -font "$font" "$@"
magick montage "$@" -tile 2x -geometry 960x540+4+4 -pointsize 18 "$out" || { echo "sheet.sh: montage failed" >&2; exit 1; }
echo "$out ($dir holds the full-size stills)"
