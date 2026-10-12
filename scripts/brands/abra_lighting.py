"""Abra Lighting (abralighting.com, Magento 2): crawl category listings -> product pages -> swatch jsonConfig.
Site returns 403 to browser User-Agents, so a plain curl-style UA is used (as observed during research)."""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from common import WORK, get

UAH = {"User-Agent": "curl/8.5.0", "Accept": "*/*"}
SITE = "https://abralighting.com"
W = WORK / "Abra_Lighting"; W.mkdir(exist_ok=True)
links = []
for cat in ("ceiling-lighting", "indoor-wall", "outdoor-wall"):
    for p in range(1, 60):
        code, body, _ = get(f"{SITE}/{cat}.html?p={p}", headers=UAH, min_interval=1.2)
        t = body.decode("utf-8", "replace") if body else ""
        new = [u for u in re.findall(r'class="product-item-link"\s+href="([^"]+)"', t) if u not in links]
        print(cat, p, code, len(new), flush=True)
        if not new:
            break
        links += new
print("product pages", len(links))

def clean(u):
    return u.replace("\\/", "/").split("?")[0]

out = []
for n, url in enumerate(links):
    code, body, _ = get(url, headers=UAH, min_interval=1.0)
    if code != 200:
        print("FAIL", code, url); continue
    t = body.decode("utf-8", "replace")
    title = re.search(r'<span class="base"[^>]*>([^<]+)', t)
    title = title.group(1).strip() if title else url
    m = re.search(r'"jsonConfig":\s*(\{.*?\}),\s*"jsonSwatchConfig"', t, re.S)
    gal = re.search(r'"data":\s*(\[\{"thumb".*?\])\s*,\s*"options"', t, re.S)
    gallery = [clean(x["full"]) for x in json.loads(gal.group(1))] if gal else []
    if m:
        d = json.loads(m.group(1))
        opts = [a["label"].rstrip(":").replace(" option", "") for a in d["attributes"].values()]
        variants, images = [], []
        for eid, sku in d.get("sku", {}).items():
            attrs = {a["label"].rstrip(":"): o["label"] for a in d["attributes"].values() for o in a["options"] if eid in o["products"]}
            imgs = [clean(x["full"]) for x in d.get("images", {}).get(eid, [])]
            variants.append(dict(sku=sku, title=", ".join(attrs.values()), attrs=attrs, image=imgs[0] if imgs else None))
            images += [dict(url=u, variant_skus=[sku]) for u in imgs]
        merged = {}
        for im in images:
            merged.setdefault(im["url"], set()).update(im["variant_skus"])
        imgs_all = [dict(url=u, variant_skus=sorted(s)) for u, s in merged.items()]
        imgs_all += [dict(url=u, variant_skus=[]) for u in gallery if u not in merged]
    else:
        sku = re.search(r'itemprop="sku"[^>]*>([^<]+)', t)
        opts = []; variants = [dict(sku=sku.group(1).strip() if sku else "", title="", attrs={}, image=None)]
        imgs_all = [dict(url=u, variant_skus=[]) for u in gallery]
    out.append(dict(pid=url, title=title, url=url, source="abralighting.com", options=opts, variants=variants, images=imgs_all))
    if n % 25 == 0:
        print(n, title, len(variants), len(imgs_all), flush=True)
json.dump(out, open(W / "catalog.json", "w"), indent=1)
(W / "sources.txt").write_text("abralighting.com (official, Magento 2): all products in ceiling-lighting, indoor-wall, outdoor-wall "
                               "category listings; per-finish child SKUs and their images from each product page's swatch configuration.")
print("products", len(out), "variants", sum(len(p["variants"]) for p in out))
