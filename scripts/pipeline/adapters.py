"""Catalog harvesters. Each returns a list of products in one unified schema:

{ "pid", "title", "url", "source",
  "options": [option names],
  "variants": [{"sku", "title", "attrs": {name: value}, "image": url|None}],
  "images":   [{"url", "variant_skus": [skus the source links this image to]}] }
"""
import html, json, re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from common import assert_allowed, get


def _clean(u):
    if not u:
        return None
    u = u.split("?")[0]
    if u.startswith("//"):
        u = "https:" + u
    return assert_allowed(u)


def shopify(site, max_pages=400, collection=None, vendor=None, log=print):
    """Harvest a Shopify store via /products.json (public storefront JSON)."""
    site = site.rstrip("/")
    base = f"{site}/collections/{collection}/products.json" if collection else f"{site}/products.json"
    out = []
    for page in range(1, max_pages + 1):
        code, data, _ = get(f"{base}?limit=250&page={page}", as_json=True, min_interval=1.0)
        if code != 200 or not data or not data.get("products"):
            if code != 200:
                log(f"  shopify page {page}: HTTP {code}")
            break
        for p in data["products"]:
            if vendor and vendor.lower() not in (p.get("vendor") or "").lower():
                continue
            imgs = {i["id"]: i for i in p.get("images", [])}
            vid_sku = {v["id"]: (v.get("sku") or "") for v in p.get("variants", [])}
            opts = [o["name"] for o in p.get("options", [])]
            variants = []
            for v in p.get("variants", []):
                im = v.get("featured_image") or imgs.get(v.get("image_id"))
                attrs = {opts[i]: v.get(f"option{i + 1}") for i in range(len(opts)) if v.get(f"option{i + 1}")}
                variants.append(dict(sku=v.get("sku") or "", title=v.get("title"), attrs=attrs,
                                     image=_clean(im["src"]) if im else None))
            images = [dict(url=_clean(i["src"]), variant_skus=[vid_sku.get(x, "") for x in i.get("variant_ids", [])])
                      for i in p.get("images", [])]
            out.append(dict(pid=str(p["id"]), title=p["title"], url=f"{site}/products/{p['handle']}",
                            source=urlparse(site).netloc, vendor=p.get("vendor"), options=opts,
                            variants=variants, images=images))
        log(f"  shopify page {page}: total products {len(out)}")
    return out


def woocommerce(site, log=print):
    """Harvest a WooCommerce store via the public Store API (incl. variations)."""
    site = site.rstrip("/")
    raw = []
    page = 1
    while True:
        code, data, hdr = get(f"{site}/wp-json/wc/store/v1/products?per_page=100&page={page}", as_json=True, min_interval=0.6)
        if code != 200 or not data:
            break
        raw += data
        log(f"  woo page {page}: {len(raw)} / {hdr.get('X-WP-Total')}")
        if len(data) < 100:
            break
        page += 1
    var_ids = [v["id"] for p in raw if p.get("type") == "variable" for v in p.get("variations", [])]

    def fetch(i):
        code, d, _ = get(f"{site}/wp-json/wc/store/v1/products/{i}", as_json=True, min_interval=0.3)
        return i, d if code == 200 else None
    vars_ = {}
    with ThreadPoolExecutor(3) as ex:
        for i, d in ex.map(fetch, var_ids):
            if d:
                vars_[i] = d
    out = []
    for p in raw:
        variants = []
        imgs = [dict(url=_clean(i["src"]), variant_skus=[]) for i in p.get("images", [])]
        if p.get("type") == "variable":
            opts = [a["name"] for a in p.get("attributes", []) if a.get("has_variations")]
            for v in p.get("variations", []):
                d = vars_.get(v["id"])
                if not d:
                    continue
                attrs = {a["name"]: a["value"] for a in v.get("attributes", [])}
                vimg = _clean(d["images"][0]["src"]) if d.get("images") else None
                variants.append(dict(sku=d.get("sku") or "", title=d.get("variation") or "", attrs=attrs, image=vimg))
                if vimg:
                    for im in imgs:
                        if im["url"] == vimg:
                            im["variant_skus"].append(d.get("sku") or "")
        else:
            opts = []
            variants.append(dict(sku=p.get("sku") or "", title="", attrs={}, image=None))
        out.append(dict(pid=str(p["id"]), title=html.unescape(p["name"]), url=p["permalink"], source=urlparse(site).netloc,
                        options=opts, variants=variants, images=imgs))
    return out


def jsonld_product(url):
    """Parse one product page: JSON-LD Product (sku, image, offers) with og:image fallback."""
    code, body, _ = get(url, min_interval=0.5)
    if code != 200 or not body:
        return None
    text = body.decode("utf-8", "replace")
    prods = []
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', text, re.S | re.I):
        try:
            d = json.loads(m.group(1).strip())
        except Exception:
            continue
        stack = d if isinstance(d, list) else [d]
        while stack:
            x = stack.pop()
            if isinstance(x, dict):
                if x.get("@type") in ("Product", ["Product"]):
                    prods.append(x)
                stack += [v for v in x.values() if isinstance(v, (dict, list))]
            elif isinstance(x, list):
                stack += x
    return dict(url=url, products=prods, html=text)
