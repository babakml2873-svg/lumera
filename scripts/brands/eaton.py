"""Eaton & Cutler-Hammer (eaton.com, Adobe AEM). Per SKU: skuPage JSON-LD (sku must equal the list SKU) -> image asset
names from the page's mdmfiles links -> full-size images from Eaton's Scene7 server dynamicmedia.eaton.com.
robots.txt Crawl-delay 20 s is respected for eaton.com pages. Resumable (raw pages cached).
usage: eaton.py "<Brand>" [...more brands]"""
import json, re, sys, time
from pathlib import Path
import requests
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from common import WORK, load_rows, slug

H = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
     "Accept-Language": "en-US,en;q=0.9", "sec-ch-ua": '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
     "sec-ch-ua-mobile": "?0", "sec-ch-ua-platform": '"macOS"', "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate",
     "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1"}
for brand in sys.argv[1:]:
    W = WORK / slug(brand); raw = W / "raw"; raw.mkdir(parents=True, exist_ok=True)
    skus = sorted({r["SKU"].strip().lstrip("'").strip() for r in load_rows(brand)})
    out = []
    for n, s in enumerate(skus):
        f = raw / (re.sub(r"[^A-Za-z0-9._-]", "_", s) + ".html")
        url = f"https://www.eaton.com/us/en-us/skuPage.{s}.html"
        if not f.exists():
            body = b""
            for attempt in range(2):
                try:
                    r = requests.get(url, headers=H, timeout=60)
                    body = r.content if r.status_code == 200 else f"HTTP {r.status_code}".encode()
                    break
                except Exception as e:
                    body = f"ERR {e}".encode()
                    time.sleep(20)
            f.write_bytes(body)
            time.sleep(20)
        t = f.read_text("utf-8", "replace")
        skus_ld = re.findall(r'"sku"\s*:\s*"([^"]+)"', t)
        if not any(x.strip().upper() == s.upper() for x in skus_ld):
            continue
        assets = list(dict.fromkeys(re.findall(r'/mdmfiles/[^/"]+/([^/"]+)/1000x1000_300dpi', t)))
        title = re.search(r'<title>([^<]+)', t)
        imgs = [f"https://dynamicmedia.eaton.com/is/image/eaton/{a}?wid=1000&hei=1000&fmt=jpg&qlt=95" for a in assets]
        fam = [a for a in assets if s.upper().replace("-", "") not in a.upper().replace("-", "")]
        out.append(dict(pid=s, title=(title.group(1).strip() if title else s), url=url, source="eaton.com", options=[],
                        family_image=bool(assets) and len(fam) == len(assets), assets=assets,
                        variants=[dict(sku=s, title="", attrs={}, image=None)], images=[dict(url=u, variant_skus=[]) for u in imgs]))
        if n % 20 == 0:
            print(brand, n, len(out), flush=True)
    json.dump(out, open(W / "catalog_1_official.json", "w"))
    (W / "sources.txt").write_text("eaton.com (official; Cutler-Hammer is an Eaton brand): product page skuPage.<SKU>.html per SKU, JSON-LD sku must equal "
                                   "the list SKU; images = the page's product image assets, downloaded full size from Eaton's image server "
                                   "dynamicmedia.eaton.com. Pages fetched at robots.txt Crawl-delay (20 s).")
    print(brand, "SKUs", len(skus), "pages with matching sku", len(out), "with images", sum(1 for p in out if p["images"]),
          "family-image only", sum(1 for p in out if p["family_image"]))
