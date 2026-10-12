"""Probe deterministic per-SKU image URLs (no catalog API available) and build a unified catalog.
usage: harvest_template.py "<Brand>" <out.json> <source-domain> <page-template> <img-template> [<extra-img-template> ...]
Templates use {sku} (apostrophe-stripped list SKU) and {sku_lower}. Only HTTP 200 + image/* responses are accepted."""
import json, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import requests
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from common import HEADERS, assert_allowed, load_rows

brand, out, domain, page_t, img_t, *extra = sys.argv[1:]
skus = sorted({r["SKU"].strip().lstrip("'").strip() for r in load_rows(brand)})

def probe(u):
    assert_allowed(u)
    for attempt in range(3):
        try:
            r = requests.get(u, headers={**HEADERS, "Range": "bytes=0-2047"}, timeout=40, stream=True)
            ct = r.headers.get("Content-Type", ""); r.close()
            if r.status_code in (200, 206) and ct.startswith("image/"):
                return True
            if r.status_code in (404, 403, 410) or "text/html" in ct:
                return False
        except Exception:
            time.sleep(2 * (attempt + 1))
    return False

def one(s):
    f = dict(sku=s, sku_lower=s.lower())
    main = img_t.format(**f)
    time.sleep(0.3)
    if not probe(main):
        return None
    imgs = [main] + [t.format(**f) for t in extra if probe(t.format(**f))]
    return dict(pid=s, title=s, url=page_t.format(**f), source=domain, options=[],
                variants=[dict(sku=s, title="", attrs={}, image=None)], images=[dict(url=u, variant_skus=[]) for u in imgs])

with ThreadPoolExecutor(3) as ex:
    res = [p for p in ex.map(one, skus) if p]
Path(out).parent.mkdir(parents=True, exist_ok=True)
json.dump(res, open(out, "w"))
print(brand, "SKUs", len(skus), "with image", len(res))
