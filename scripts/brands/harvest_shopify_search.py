"""Per-SKU Shopify search: /search/suggest.json?q=<SKU> -> /products/<handle>.json; keep products with a variant whose sku equals
the list SKU (case/punctuation-insensitive). usage: harvest_shopify_search.py "<Brand>" <site> <out.json> [--skip-regex RE]"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from adapters import _clean
from common import get, load_rows, match_key
from urllib.parse import urlparse, quote

brand, site, out = sys.argv[1:4]
skip = re.compile(sys.argv[sys.argv.index("--skip-regex") + 1]) if "--skip-regex" in sys.argv else None
site = site.rstrip("/")
skus = sorted({r["SKU"].strip().lstrip("'").strip() for r in load_rows(brand)})
res, seen = [], set()
for n, s in enumerate(skus):
    code, d, _ = get(f"{site}/search/suggest.json?q={quote(s)}&resources[type]=product&resources[limit]=6", as_json=True, min_interval=0.8)
    hs = [p["url"].split("?")[0].split("/products/")[-1] for p in ((d or {}).get("resources", {}).get("results", {}).get("products", []) if code == 200 else [])]
    for h in hs:
        if h in seen:
            continue
        c2, pj, _ = get(f"{site}/products/{h}.json", as_json=True, min_interval=0.8)
        p = (pj or {}).get("product") if c2 == 200 else None
        if not p:
            continue
        vs = [v for v in p["variants"] if match_key(v.get("sku") or "") == match_key(s) and not (skip and skip.search(v.get("sku") or ""))]
        if not vs:
            continue
        seen.add(h)
        imgs = {i["id"]: i for i in p.get("images", [])}
        vid_sku = {v["id"]: (v.get("sku") or "") for v in p["variants"]}
        opts = [o["name"] for o in p.get("options", [])]
        variants = [dict(sku=v.get("sku") or "", title=v.get("title"),
                         attrs={opts[i]: v.get(f"option{i+1}") for i in range(len(opts)) if v.get(f"option{i+1}")},
                         image=_clean((v.get("featured_image") or imgs.get(v.get("image_id")) or {}).get("src")))
                    for v in p["variants"] if not (skip and skip.search(v.get("sku") or ""))]
        res.append(dict(pid=str(p["id"]), title=p["title"], url=f"{site}/products/{h}", source=urlparse(site).netloc, vendor=p.get("vendor"),
                        options=opts, variants=variants,
                        images=[dict(url=_clean(i["src"]), variant_skus=[vid_sku.get(x, "") for x in i.get("variant_ids", [])]) for i in p.get("images", [])]))
        break
    if n % 50 == 0:
        print(n, len(res), flush=True)
Path(out).parent.mkdir(parents=True, exist_ok=True)
json.dump(res, open(out, "w"))
print(brand, site, "SKUs", len(skus), "matched products", len(res))
