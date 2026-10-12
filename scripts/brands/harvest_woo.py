"""Harvest a WooCommerce store (Store API incl. variations) into the unified format.
usage: harvest_woo.py <site> <out.json> [--name-as-sku]  (--name-as-sku: product name used as SKU when the sku field is empty)"""
import html, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from adapters import woocommerce
P = woocommerce(sys.argv[1], log=lambda m: None)
if "--name-as-sku" in sys.argv:
    for p in P:
        for v in p["variants"]:
            if not v["sku"] and len(p["variants"]) == 1:
                v["sku"] = html.unescape(p["title"]).strip()
Path(sys.argv[2]).parent.mkdir(parents=True, exist_ok=True)
json.dump(P, open(sys.argv[2], "w"))
print(sys.argv[1], "products", len(P), "variants", sum(len(p["variants"]) for p in P), "with sku", sum(1 for p in P for v in p["variants"] if v["sku"]))
