"""Custom official-site harvesters: Westinghouse Lighting, Utopia Lighting.  usage: custom_c.py <key>"""
import json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import requests
from custom_a import prod, save, skus_of
from common import HEADERS, get, match_key

k = sys.argv[1]
if k == "westinghouse":
    b = "Westinghouse Lighting"; items = {}
    ids = list(range(300, 371))
    for cid in ids:
        r = requests.post("https://www.westinghouselighting.com/includes/Webservices/GetProducts.asmx/GetProductPackage",
                          json={"SiteObjectId": str(cid), "mySearchOptions": [], "myTotals": [], "ResultsPerPage": 1000, "DesiredPage": 1, "AllItems": "true"},
                          headers={**HEADERS, "Content-Type": "application/json"}, timeout=60)
        try:
            pl = (r.json().get("d") or {}).get("ProductList") or []
        except Exception:
            pl = []
        for p in pl:
            items.setdefault(str(p.get("ItemNumber")).strip(), p)
    print("items", len(items))
    out = []
    for s in skus_of(b):
        p = items.get(s)
        if not p:
            continue
        img = p.get("PrimaryMediumImage") or ""
        img = re.sub(r"-(sm|md)\.jpg$", "-lg.jpg", img)
        img = img if img.startswith("http") else "https://www.westinghouselighting.com" + ("" if img.startswith("/") else "/") + img
        url = p.get("Url") or ""
        url = url if url.startswith("http") else "https://www.westinghouselighting.com" + ("" if url.startswith("/") else "/") + url
        out.append(prod(s, p.get("Title") or s, url, "westinghouselighting.com", [img] if p.get("PrimaryMediumImage") else []))
    save(b, out, "westinghouselighting.com (official): the site's product-list web service (GetProductPackage, all product categories) - "
                 "ItemNumber must equal the list SKU; primary product image in large size (-lg.jpg).")
elif k == "utopia":
    b = "Utopia Lighting"; out = []
    for s in skus_of(b):
        code, d, _ = get(f"https://utopialighting.com/search/ajax?q={requests.utils.quote(s)}", as_json=True, min_interval=1.0)
        hits = (d or {}).get("hits") or [] if isinstance(d, dict) else []
        for h in hits:
            if h.get("item_type") != "product":
                continue
            name = str(h.get("model") or "")
            if match_key(name) == match_key(s):
                img = (h.get("image") or "").replace("/medium/", "/original/")
                url = "https://utopialighting.com/product/" + h.get("slug", "")
                out.append(prod(s, h.get("product_title") or name, url, "utopialighting.com", [img] if img else []))
                break
    save(b, out, "utopialighting.com (official): the site's JSON search /search/ajax?q=<model>, model name must equal the list SKU "
                 "(punctuation/case-insensitive); original-size product image.")

if k == "euri":
    b = "Euri Lighting"; card = {}
    for pg in range(1, 7):
        code, body, _ = get(f"https://www.euricompany.com/products?feaebd7c_page={pg}", min_interval=1.0)
        t = body.decode("utf-8", "replace") if body else ""
        n0 = len(card)
        for blk in t.split('role="listitem"')[1:]:
            skus = [x.strip() for x in re.findall(r'fs-cmsfilter-field="sku\d"[^>]*>([^<]+)<', blk)]
            href = re.search(r'href="(/products/[^"]+)"', blk)
            for s_ in skus:
                if href:
                    card.setdefault(match_key(s_), (s_, "https://www.euricompany.com" + href.group(1)))
        print("page", pg, len(card), flush=True)
        if len(card) == n0:
            break
    pages = {}
    def og(url):
        if url not in pages:
            c, bd, _ = get(url, min_interval=1.0)
            tt = bd.decode("utf-8", "replace") if bd and c == 200 else ""
            m = re.search(r'property="og:image"\s+content="([^"]+)"', tt) or re.search(r'content="([^"]+)"\s+property="og:image"', tt)
            ti = re.search(r"<title>([^<]+)", tt)
            pages[url] = (m.group(1) if m else None, ti.group(1).strip() if ti else "")
        return pages[url]
    out = []
    for s in skus_of(b):
        hit = card.get(match_key(s))
        if not hit:
            c, bd, _ = get(f"https://www.euricompany.com/search?query={requests.utils.quote(s)}", min_interval=1.0)
            tt = bd.decode("utf-8", "replace") if bd else ""
            for h in re.findall(r'href="(/products/[^"]+)"', tt):
                if h.rstrip("/").lower().endswith(s.lower()):
                    hit = (s, "https://www.euricompany.com" + h); break
        if not hit:
            continue
        img, title = og(hit[1])
        if img:
            out.append(prod(s, title or s, hit[1], "euricompany.com", [img]))
    save(b, out, "euricompany.com (official Euri Lighting; eurilighting.com redirects there, Webflow site): product listing cards (each lists up "
                 "to 5 SKUs) and site search; product page og:image. SKUs sharing one product page (colour-temperature variants) share "
                 "its image and are marked Medium.")
