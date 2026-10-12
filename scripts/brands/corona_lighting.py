"""Corona Lighting (coronalighting.com, WooCommerce Store API). Finish SKUs live in the variation attribute
'Fixture Number' / 'Lamp Number' (the variation sku field is sometimes wrong), so that attribute is used as the SKU."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from adapters import woocommerce
from common import WORK
W = WORK / "Corona_Lighting"; W.mkdir(exist_ok=True)
P = woocommerce("https://coronalighting.com", log=lambda m: None)
n = 0
for p in P:
    for v in p["variants"]:
        num = next((val for k, val in v["attrs"].items() if re.search(r"fixture number|lamp number|item number|model", k, re.I)), None)
        if num:
            if v["sku"] and v["sku"] != num:
                v["site_sku_field"] = v["sku"]
            v["sku"] = num.strip(); n += 1
        elif not v["sku"] and len(p["variants"]) == 1:
            m = re.match(r"\s*([A-Z0-9][A-Z0-9.\-/]+)", p["title"].upper())
            v["sku"] = m.group(1) if m else ""
    # images were linked to the variation 'sku' field; relink to the attribute-based SKU
    for im in p["images"]:
        im["variant_skus"] = [v["sku"] for v in p["variants"] if v.get("image") == im["url"]]
json.dump(P, open(W / "catalog_1_official.json", "w"))
(W / "sources.txt").write_text("coronalighting.com (official, WooCommerce Store API incl. every variation): finish SKU taken from the variation "
                               "attribute 'Fixture Number'/'Lamp Number'; variation-linked images.")
print("products", len(P), "variants", sum(len(p["variants"]) for p in P), "attr-sku", n)
