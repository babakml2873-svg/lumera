#!/usr/bin/env bash
# Finish one brand after its catalog(s) are harvested into work/<slug>/catalog*.json:
#   process images -> README -> consolidated reports + brand ZIP -> commit -> push (retry with backoff)
# usage: scripts/pipeline/finish_brand.sh "<Brand>" [--skip-process]
set -euo pipefail
BRAND="$1"; shift || true
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT/scripts/pipeline"
SLUG=$(python3 -c "import sys; from common import slug; print(slug(sys.argv[1]))" "$BRAND")
if [[ "${1:-}" != "--skip-process" ]]; then
  python3 run_brand.py "$BRAND"
fi
python3 make_readme.py "$BRAND" > /dev/null
python3 reports.py --zip "$BRAND" | tail -3
cd "$ROOT"
git add .gitignore .gitattributes scripts Output "work/$SLUG" work/_all
git commit -q -m "Add product images for brand: $BRAND

Images, consolidated reports and verified ZIP (Git LFS) for $BRAND.
Sources: see work/$SLUG/sources.txt. Lumera Electric was not used as a source.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Kp9744m7VBH5aWnLL9tRuJ" || echo "nothing to commit"
for d in 0 2 4 8 16; do
  sleep $d
  if git push -u origin claude/product-image-crawling-git-h0756k 2>&1 | tail -3; then
    if [[ "$(git ls-remote origin claude/product-image-crawling-git-h0756k | cut -f1)" == "$(git rev-parse HEAD)" ]]; then
      echo "PUSHED $(git rev-parse HEAD)"; break
    fi
  fi
done
rm -rf "work/$SLUG/cache"
du -sh .git | cut -f1 | sed 's/^/git size: /'
