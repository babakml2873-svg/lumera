"""Custom official-site harvesters: Damar, Enerlites, EnVision, EMCOD.  usage: custom_a.py <brand-key>"""
import json, re, sys, html as H
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
import requests
from common import WORK, get, load_rows, match_key, slug, HEADERS

def skus_of(brand):
    return sorted({r["SKU"].strip().lstrip("'").strip() for r in load_rows(brand)})

def prod(sku, title, url, source, imgs, assets=None):
    k = match_key(sku)
    fam = bool(imgs) and not any(k in match_key(Path(u).stem) for u in imgs)
    return dict(pid=sku, title=title, url=url, source=source, options=[], family_image=fam,
                assets=[Path(u).name for u in imgs][:2], variants=[dict(sku=sku, title="", attrs={}, image=None)],
                images=[dict(url=u, variant_skus=[]) for u in imgs])

def save(brand, out, src):
    W = WORK / slug(brand); W.mkdir(exist_ok=True)
    json.dump(out, open(W / "catalog_1_official.json", "w")); (W / "sources.txt").write_text(src)
    print(brand, "records", len(out), "with images", sum(1 for p in out if p["images"]), "family-image", sum(1 for p in out if p["family_image"]))

which = sys.argv[1]
if which == "damar":
    b = "Damar"; out = []
    for s in skus_of(b):
        url = f"https://damarww.com/products/details/di/x/{s}/"
        code, body, _ = get(url, min_interval=1.0)
        t = body.decode("utf-8", "replace") if body else ""
        sku_ok, imgs, title = False, [], s
        for m in re.finditer(r'<script[^>]+ld\+json[^>]*>(.*?)</script>', t, re.S):
            try: d = json.loads(m.group(1))
            except Exception: continue
            for x in (d if isinstance(d, list) else [d]):
                if isinstance(x, dict) and x.get("@type") == "Product" and match_key(str(x.get("sku", ""))) == match_key(s):
                    sku_ok = True; title = x.get("name", s)
                    im = x.get("image"); imgs += im if isinstance(im, list) else ([im] if im else [])
        if sku_ok:
            imgs = [u if u.startswith("http") else "https://damarww.com/" + u.lstrip("/") for u in dict.fromkeys(imgs)]
            out.append(prod(s, title, url, "damarww.com", imgs))
    save(b, out, "damarww.com (official Damar Worldwide; damarworldwide.com does not resolve): product page /products/details/di/x/<SKU>/ per SKU, "
                 "JSON-LD Product sku must equal the list SKU; JSON-LD image(s).")
elif which == "enerlites":
    b = "Enerlites"
    code, body, _ = get("https://www.enerlites.com/products", min_interval=1.0)
    t = body.decode("utf-8", "replace").replace('\\"', '"')
    base = "https://nokxwrrxvvnplxehxvuh.supabase.co/storage/v1/object/public/product-assets/"
    byfile, bymodel = {}, {}
    for m in re.finditer(r'"model_number":"([^"]*)","slug":"([^"]+)","title":"([^"]*)"', t):
        model, sl, title = m.groups()
        seg = t[m.end(): m.end() + 20000]
        mm = re.search(r'"media":\[(.*?)\]', seg)
        media = re.findall(r'"([^"]+\.(?:png|jpg|jpeg|webp))"', mm.group(1)) if mm else []
        for f in media:
            code_ = Path(f).name.split("_")[0]
            byfile.setdefault(match_key(code_), []).append((base + f, sl, title))
        bymodel.setdefault(match_key(model), [(base + f, sl, title) for f in media])
    out = []
    for s in skus_of(b):
        hits = byfile.get(match_key(s))
        if hits:
            imgs = sorted(dict.fromkeys(h[0] for h in hits), key=lambda u: (not u.endswith("_1.png"), u))
            out.append(prod(s, hits[0][2], f"https://www.enerlites.com/products/{hits[0][1]}", "enerlites.com", imgs))
    save(b, out, "enerlites.com (official): /products page data (all 584 products) - image files are named <colour SKU>_<colour>_<n>, "
                 "so each list SKU is matched to the images named with exactly that SKU (2400x2400 originals).")
elif which == "envision":
    b = "EnVision"; out = []
    sk = skus_of(b)
    for i in range(0, len(sk), 80):
        q = {"query": "query($n:[String]){allProducts(first:100, filter:{number:{in:$n}}){number slug name images{url width height}}}",
             "variables": {"n": sk[i:i + 80]}}
        r = requests.post("https://graphql.datocms.com/", json=q, headers={**HEADERS, "Authorization": "Bearer 50a703e5c3903699f5ca2a6edbe026"}, timeout=60)
        for p in r.json().get("data", {}).get("allProducts", []):
            imgs = [x["url"] for x in p.get("images") or []]
            out.append(prod(p["number"], p.get("name") or p["number"], f"https://www.envisionledlighting.com/products/{p['slug']}", "envisionledlighting.com", imgs))
        print(i, len(out), flush=True)
    save(b, out, "envisionledlighting.com (official EnVision LED Lighting): the site's own DatoCMS content API queried by part number "
                 "(field 'number' = full SKU); product images as published (originals ~1200 px).")
elif which == "emcod":
    b = "EMCOD Lighting Group"
    code, body, _ = get("https://www.emcod.com/products", min_interval=1.0)
    t = body.decode("utf-8", "replace")
    ids = {}
    for pid, name in re.findall(r'class="product_link"[^>]*href="/products/info\?id=(\d+)&?">([^<]+)</a>', t):
        ids.setdefault(match_key(H.unescape(name).replace(" T24", "")), (pid, H.unescape(name).strip()))
    out, cache = [], {}
    for s in skus_of(b):
        hit = ids.get(match_key(s))
        if not hit: continue
        pid, name = hit
        if pid not in cache:
            c, bd, _ = get(f"https://www.emcod.com/products/info?id={pid}", min_interval=1.0)
            tt = bd.decode("utf-8", "replace") if bd else ""
            m = re.search(r'<div class="product_img">\s*<a href="([^"]+)"', tt)
            cache[pid] = ["https://www.emcod.com" + m.group(1)] if m else []
        p = prod(s, name, f"https://www.emcod.com/products/info?id={pid}", "emcod.com", cache[pid])
        p["family_image"] = sum(1 for v in ids.values() if v[0] == pid) > 1
        out.append(p)
    save(b, out, "emcod.com (official): /products model list -> product page /products/info?id=N; main product image (div.product_img). "
                 "Several models share one page/image; those are marked Medium.")
