"""American Lighting (americanlighting.com, Magento 2): public GraphQL, queried by the list SKUs in batches."""
import json, sys, urllib.parse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "pipeline"))
from common import WORK, get, load_rows

W = WORK / "American_Lighting"; W.mkdir(exist_ok=True)
skus = sorted({r["SKU"].strip().lstrip("'").strip() for r in load_rows("American Lighting")})
out = []
for i in range(0, len(skus), 40):
    batch = skus[i:i + 40]
    q = ('{products(filter:{sku:{in:[%s]}},pageSize:100){items{sku name url_key image{url} media_gallery{url disabled position}}}}'
         % ",".join(json.dumps(s) for s in batch))
    code, d, _ = get("https://americanlighting.com/graphql?query=" + urllib.parse.quote(q), as_json=True, min_interval=1.0)
    items = (d or {}).get("data", {}).get("products", {}).get("items", []) if code == 200 else []
    print(i, code, len(items), flush=True)
    for it in items:
        gal = sorted([g for g in it.get("media_gallery") or [] if not g.get("disabled")], key=lambda g: g.get("position") or 0)
        urls = [u.split("?")[0] for u in [(it.get("image") or {}).get("url")] + [g["url"] for g in gal] if u]
        urls = [u for u in dict.fromkeys(urls) if "/placeholder/" not in u and "accessory_ph" not in u]
        out.append(dict(pid=it["sku"], title=it["name"], url=f"https://americanlighting.com/{it['url_key']}", source="americanlighting.com",
                        options=[], variants=[dict(sku=it["sku"], title="", attrs={}, image=None)],
                        images=[dict(url=u, variant_skus=[]) for u in urls]))
json.dump(out, open(W / "catalog_1_official.json", "w"))
(W / "sources.txt").write_text("americanlighting.com (official, Magento 2): public GraphQL products(filter:{sku:{in:[...]}}) queried for every list SKU; "
                               "main image + media gallery; placeholder/generic accessory images excluded.")
print("items", len(out), "with images", sum(1 for p in out if p["images"]), "of", len(skus))
