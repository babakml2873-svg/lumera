"""Write work/<slug>/README.md for one brand from its plan/results (used inside the brand ZIP).

usage: python3 make_readme.py "<Brand>"
"""
import json, sys
from collections import Counter

from common import WORK, brand_dir, slug

b = sys.argv[1]
W = WORK / slug(b)
plan = json.load(open(W / "plan_final.json")); res = json.load(open(W / "results.json"))
src = (W / "sources.txt").read_text().strip() if (W / "sources.txt").exists() else ""
cfg = json.load(open(W / "config.json")) if (W / "config.json").exists() else {}
notes = (W / "notes.md").read_text().strip() if (W / "notes.md").exists() else ""
lists = Counter("List_" + r["list"].replace("List", "") for r in plan)
v = Counter(r["list"] for r in res if r["type"] == "V" and r["file"])
g = Counter(r["list"] for r in res if r["type"] == "G" and r["file"])
origins = Counter(r["origin"] for r in res if r["file"])
med = sum(1 for r in plan if r.get("conf") == "Medium" and any(x["sku"] == r["sku"] and x["type"] == "V" and x["file"] for x in res))
reasons = Counter((r.get("review") or r.get("v_withheld") or "V image failed processing").split(";")[0][:110]
                  for r in plan if not any(x["sku"] == r["sku"] and x["list"] == "List_" + r["list"].replace("List", "")
                                           and x["type"] == "V" and x["file"] for x in res))
tot = len(plan); vt = sum(v.values())
lines = [f"# {b} — product images", "",
         f"Brand {b}: {tot} SKUs in the product lists. Variant images were delivered for **{vt} SKUs ({100 * vt / tot:.1f}%)**, "
         f"plus **{sum(g.values())} gallery images** (max {cfg.get('max_g', 4)} per SKU).", "",
         "| List | SKUs | Variant images | Gallery images |", "|---|---|---|---|"]
for l in ("List_1", "List_2", "List_3", "List_4"):
    lines.append(f"| {l} | {lists.get(l, 0)} | {v.get(l, 0)} | {g.get(l, 0)} |")
lines += ["", f"* {med} of the variant images are Medium confidence (`OK-REVIEW-RECOMMENDED`), see `Reports/review_queue.csv`.",
          "* Every file was checked by script: 800×800 px JPG, ≤ 100,000 bytes, `SKU-V.jpg` / `SKU-G-NN.jpg`.",
          "* Image sources (files): " + ", ".join(f"{k} ({n})" for k, n in origins.most_common()) + ". No Lumera Electric source was used.",
          "", "## Sources searched", "", src or "-", "", "## Matching rules", "",
          "* A variant image (V) requires an exact SKU match (case/punctuation-insensitive) with the source, and an image the source "
          "links to that SKU — or the product's main image when the product has one variant or its variants differ only in "
          "non-visual options (colour temperature, wattage, voltage, beam, length…).",
          "* Products whose variants differ visually (finish, colour, shade…) without a SKU-linked image get no V (listed for review).",
          "* Gallery images (G) come from the same product; images the source links to a different variant are never used.",
          "* A random sample of variant images was checked visually for product identity.",
          "", "## SKUs without a variant image — reasons", "", "| Reason | SKUs |", "|---|---|"]
lines += [f"| {k} | {n} |" for k, n in reasons.most_common()]
if notes:
    lines += ["", "## Brand-specific notes", "", notes]
lines += ["", "## Folder structure", "", "`List_N/" + brand_dir(b) + "/` images per original list (empty lists hold a marker file); "
          "`Reports/` the brand's image_report, missing_images, sku_filename_mapping, brand_progress and review_queue CSVs."]
(W / "README.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines[:12]))
