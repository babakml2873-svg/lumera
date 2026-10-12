"""Custom official-site harvesters: Intermatic, Leviton, Lew Electric, Morris.  usage: custom_b.py <key>"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from custom_a import prod, save, skus_of
from common import WORK, get, match_key

k = sys.argv[1]
if k == "intermatic":
    b = "Intermatic"; out = []
    for s in skus_of(b):
        code, d, _ = get(f"https://www.intermatic.com/api/v1/products?query={s}&expand=images", as_json=True, min_interval=0.8)
        for p in (d or {}).get("products", []) if code == 200 else []:
            if match_key(p.get("erpNumber", "")) != match_key(s):
                continue
            imgs = [i.get("largeImagePath") or i.get("mediumImagePath") for i in p.get("productImages", [])]
            imgs = [u if u.startswith("http") else "https://www.intermatic.com" + u for u in imgs if u] or \
                   ([p["largeImagePath"]] if p.get("largeImagePath") and "notfound" not in p["largeImagePath"].lower() else [])
            out.append(prod(s, p.get("shortDescription") or s, "https://www.intermatic.com/Product/" + s, "intermatic.com", list(dict.fromkeys(imgs))))
            break
    save(b, out, "intermatic.com (official): the site's storefront API /api/v1/products?query=<SKU>&expand=images, erpNumber must equal the list SKU; "
                 "product images as published (images named for a sibling model are marked Medium).")
elif k == "leviton":
    from concurrent.futures import ThreadPoolExecutor
    import threading
    b = "Leviton"
    code, body, _ = get("https://leviton.com/sitemap-products.xml", min_interval=1.0)
    urls = {m.rstrip("/").split("/")[-1].upper(): m for m in re.findall(r"<loc>([^<]+/products/[^<]+)</loc>", body.decode("utf-8", "replace"))}
    print("sitemap", len(urls), flush=True)
    cache_p = WORK / "Leviton" / "og_cache.jsonl"; cache_p.parent.mkdir(exist_ok=True)
    done = {}
    if cache_p.exists():
        for line in open(cache_p):
            d = json.loads(line); done[d["sku"]] = d
    todo = [s for s in skus_of(b) if s.upper() in urls and s not in done]
    print("todo", len(todo), "cached", len(done), flush=True)
    lock = threading.Lock()
    def one(s):
        u = urls[s.upper()]
        c, bd, _ = get(u, min_interval=0.3)
        t = bd.decode("utf-8", "replace") if bd else ""
        m = re.search(r'<meta[^>]+property="og:image"[^>]+content="([^"]+)"', t) or re.search(r'content="([^"]+)"[^>]+property="og:image"', t)
        title = re.search(r"<title>([^<]+)", t)
        rec = dict(sku=s, url=u, code=c, og=m.group(1) if m else None, title=title.group(1).strip() if title else s)
        if c in (200, 404):
            with lock:
                open(cache_p, "a").write(json.dumps(rec) + "\n")
        return rec
    with ThreadPoolExecutor(4) as ex:
        for n, rec in enumerate(ex.map(one, todo)):
            done[rec["sku"]] = rec
            if n % 200 == 0:
                print(n, flush=True)
    out = []
    for s in skus_of(b):
        d = done.get(s)
        if d and d.get("og") and "/product_images/" in d["og"]:
            img = d["og"] if d["og"].startswith("http") else "https://leviton.com" + d["og"]
            out.append(prod(s, d["title"], d["url"], "leviton.com", [img]))
    save(b, out, "leviton.com (official): product sitemap (18,598 product pages, page path = SKU) -> each needed product page's og:image "
                 "(main product image from Leviton's DAM).")
elif k == "lew":
    b = "Lew Electric"
    code, body, _ = get("https://lewelectric.com/catalog-sitemap.xml", min_interval=1.0)
    t = body.decode("utf-8", "replace"); m = {}
    for blk in re.findall(r"<url>(.*?)</url>", t, re.S):
        loc = re.search(r"<loc>([^<]+)</loc>", blk); imgs = re.findall(r"<image:loc>([^<]+)</image:loc>", blk)
        if loc:
            m[loc.group(1).rstrip("/").split("/")[-1].upper()] = (loc.group(1), imgs)
    out = [prod(s, s, m[s.upper()][0], "lewelectric.com", m[s.upper()][1]) for s in skus_of(b) if s.upper() in m]
    save(b, out, "lewelectric.com (official): catalog sitemap (396 product pages named by SKU) with each page's product image.")
elif k == "morris":
    b = "Morris"; out = []; sk = skus_of(b)
    for i in range(0, len(sk), 30):
        code, d, _ = get("https://morrisproducts.com/pc_product_detail.asp?key=helper&ajax=get-product-by-sku&skus=" + "~".join(sk[i:i + 30]),
                         as_json=True, min_interval=1.0)
        items = d if isinstance(d, list) else (d or {}).get("products", d.get("items", []) if isinstance(d, dict) else [])
        for p in items or []:
            s = str(p.get("sku", "")).strip()
            f = p.get("largePic") or p.get("pic")
            if s and f:
                link = p.get("link") or ""
                url = link if link.startswith("http") else "https://morrisproducts.com/" + link.lstrip("/")
                out.append(prod(s, p.get("name") or s, url, "morrisproducts.com", ["https://dehbblwvl33hy.cloudfront.net/images/" + f.lower()]))
        print(i, len(out), flush=True)
    save(b, out, "morrisproducts.com (official Morris Products): the site's own product-by-SKU JSON service; largePic image from Morris' image CDN "
                 "(900x900). Child SKUs that only show the parent family image are marked Medium.")
