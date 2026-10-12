"""Harvest a Shopify store/collection into the unified catalog format.
usage: harvest_shopify.py <site> <out.json> [--collection handle] [--vendor substring]"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from adapters import shopify
a = sys.argv
col = a[a.index("--collection") + 1] if "--collection" in a else None
ven = a[a.index("--vendor") + 1] if "--vendor" in a else None
prods = shopify(a[1], collection=col, vendor=ven, log=lambda m: None)
Path(a[2]).parent.mkdir(parents=True, exist_ok=True)
json.dump(prods, open(a[2], "w"))
print(a[1], col, ven, "products", len(prods), "variants", sum(len(p["variants"]) for p in prods),
      "with sku", sum(1 for p in prods for v in p["variants"] if v["sku"]))
