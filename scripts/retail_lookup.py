"""Look up ABBA models on Shopify-based ABBA resellers; print variant SKUs + variant images."""
import json, subprocess, sys, re
from pathlib import Path
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
OUT = Path(__file__).resolve().parent.parent / "work" / "abba" / "retail"
DOMAINS = ["sonicelectric.com", "readyelectricsupply.com", "kingsoutdoorlighting.com", "www.lbclightingpro.com"]
def get(u):
    r = subprocess.run(["curl", "-gsS", "-m", "30", "-H", f"User-Agent: {UA}", u], capture_output=True, text=True)
    return r.stdout
for q in sys.argv[1:]:
    for d in DOMAINS:
        try:
            res = json.loads(get(f"https://{d}/search/suggest.json?q={q}&resources[type]=product&resources[limit]=6"))
        except Exception:
            print("ERR", d, q); continue
        for p in res["resources"]["results"]["products"]:
            if "abba" not in (p.get("vendor") or "").lower() and "abba" not in p["title"].lower():
                continue
            if q.upper() not in re.sub(r"[^A-Z0-9]", "", p["title"].upper()):
                continue
            h = p["url"].split("?")[0].split("/products/")[1]
            raw = get(f"https://{d}/products/{h}.json")
            (OUT / f"{d}__{h}.json").write_text(raw)
            pr = json.loads(raw)["product"]
            imgs = {i["id"]: i for i in pr["images"]}
            print(f"== {q} @ {d} :: {pr['title']} ({len(pr['images'])} imgs)")
            for v in pr["variants"]:
                im = imgs.get(v.get("image_id"))
                print("    ", repr(v["sku"]), "|", v["title"], "|", (im["src"].split("/")[-1][:60], im["width"]) if im else None)
