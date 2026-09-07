#!/usr/bin/env bash
# Download every asset in ASSET-MANIFEST.json into ./assets/<episode>/<kind>/ .
# Needs: bash, curl, python3. Run from the repo root. Safe to re-run; skips files already present.
set -euo pipefail
cd "$(dirname "$0")"
python3 - <<'PY' | while read -r ep kind name url; do
import json
m=json.load(open("ASSET-MANIFEST.json"))
for ep,e in m["episodes"].items():
    for kind in ("stills","clips","voices","music","thumbnails"):
        for a in e[kind]: print(ep, kind, a["kind"], a["url"])
    print(ep, "final", "final_1080p", e["final"]["url"])
PY
  ext="${url##*.}"; out="assets/$ep/$kind/$name.$ext"; mkdir -p "$(dirname "$out")"
  if [ -s "$out" ]; then echo "skip $out"; else echo "get  $out"; curl -fsSL --retry 3 --retry-all-errors "$url" -o "$out"; fi
done
echo "done: $(find assets -type f | wc -l) files, $(du -sh assets | cut -f1)"
