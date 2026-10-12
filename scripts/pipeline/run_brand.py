"""Plan -> download -> process -> results for one brand, from its harvested catalog(s).

usage: python3 run_brand.py "<Brand>" [catalog.json ...]   (default: work/<slug>/catalog*.json in name order = priority)

Variant (V) rules - exact SKU identity is required:
  * the list SKU must equal a source variant SKU (case/punctuation-insensitive);
  * V = the image the source links to that variant; otherwise the product's main image only when the product has a
    single variant, or all its variants differ only in non-visual options (CCT, wattage, voltage, beam, length...);
  * products whose variants differ visually (finish/colour/shade...) without a variant-linked image -> V withheld.
Gallery (G): other images of the same product; images the source links to a different variant are never used, and for
products with visual variants only images linked to this variant are used. Near-duplicates removed by pHash.
"""
import glob, html, json, random, re, sys
from collections import Counter, defaultdict
from pathlib import Path

import imagehash
from PIL import Image, ImageDraw, ImageFont

from common import (MAX_G, OUT, WORK, brand_dir, download_all, file_sku, list_dir, load_rows, match_key,
                    process_file, slug)

NONVISUAL = re.compile(r"colou?r ?temp|\bcct\b|kelvin|temperature|volt|watt|lumen|beam|dimm|wire|cord|length|pack|"
                       r"\bqty\b|quantity|driver|input|output|sensor|emergency|battery|\bcri\b|distribution|"
                       r"spread|angle|lamp type|bulb type|certification|title", re.I)

brand = sys.argv[1]
W = WORK / slug(brand); W.mkdir(parents=True, exist_ok=True)
cats = sys.argv[2:] or sorted(glob.glob(str(W / "catalog*.json")))
overrides = json.load(open(W / "overrides.json")) if (W / "overrides.json").exists() else {}
config = json.load(open(W / "config.json")) if (W / "config.json").exists() else {}

# ---------------------------------------------------------------- index
products = []
for prio, c in enumerate(cats):
    for p in json.load(open(c)):
        p["_prio"] = prio
        products.append(p)
idx = defaultdict(list)
for p in products:
    for v in p["variants"]:
        if v.get("sku"):
            idx[match_key(v["sku"])].append((p, v))


# Non-visual ordering suffixes: the source lists the same fixture with an electrical/CCT option appended
# (universal voltage, 0-10V dimming, selectable CCT...). Keys are punctuation-free.
SUFFIX_OK = re.compile(config.get("suffix_regex", r"^(UNV|UNV010|010|5CCT|3CCT|CCT|120V?|277V?|12V|24V)$"))
keys_by_prefix = defaultdict(list)
for k in idx:
    keys_by_prefix[k[:4]].append(k)


def suffix_hits(k):
    c = [x for x in keys_by_prefix.get(k[:4], []) if x != k and x.startswith(k) and SUFFIX_OK.match(x[len(k):])]
    return c[0] if len(c) == 1 else None


def visual_variants(p):
    if len(p["variants"]) <= 1:
        return False
    return any(not NONVISUAL.search(o or "") for o in p.get("options", []) or ["?"])


# ---------------------------------------------------------------- plan
rows = load_rows(brand)
plan = []
for r in rows:
    s = r["SKU"]
    rec = dict(list=r["List"], brand=brand, sku=s, nsku=file_sku(s), product="", page="", conf="", note="",
               review="", resolution="", v=None, g=[])
    o = overrides.get(s, {})
    hits = idx.get(match_key(s), [])
    suffix_key = None
    if not hits and not o.get("review"):
        suffix_key = suffix_hits(match_key(s))
        hits = idx.get(suffix_key, []) if suffix_key else []
    if o.get("review"):
        rec["review"] = o["review"]
    elif not hits:
        rec["review"] = "No exact SKU match in the harvested source catalog(s)"
    else:
        hits.sort(key=lambda t: (t[0]["_prio"], t[1].get("image") is None))
        p, v = hits[0]
        others = len({id(h[0]) for h in hits}) - 1
        rec.update(product=html.unescape(p["title"]), page=p["url"], resolution=f"exact-SKU@{p['source']}",
                   conf="High", note=f"Exact source SKU '{v['sku']}'" + (f" [{v['title']}]" if v.get("title") else ""))
        if suffix_key:
            rec["conf"] = "Medium"
            rec["note"] = (f"Source lists this item only as '{v['sku']}' (same fixture with an electrical/CCT ordering suffix)"
                           + (f" [{v['title']}]" if v.get("title") else ""))
        if p.get("family_image"):
            rec["conf"] = "Medium"
            rec["note"] += ("; the source shows a product-family image on this SKU's page (asset "
                            + ", ".join(p.get("assets", [])[:2]) + "), not one named for this exact SKU")
        if others:
            rec["note"] += f"; SKU also listed on {others} other product page(s) - first by source priority used"
        vis = visual_variants(p)
        linked_other = {im["url"] for im in p["images"] if im["variant_skus"] and v["sku"] not in im["variant_skus"]}
        own = [im["url"] for im in p["images"] if v["sku"] and v["sku"] in im["variant_skus"]]
        unlinked = [im["url"] for im in p["images"] if not im["variant_skus"]]
        if v.get("image"):
            rec["v"] = dict(url=v["image"], page=p["url"], origin=p["source"], kind="source image linked to this SKU")
        elif not vis and p["images"]:
            rec["v"] = dict(url=p["images"][0]["url"], page=p["url"], origin=p["source"], kind="product main image")
            if len(p["variants"]) > 1:
                rec["conf"] = "Medium"
                rec["note"] += "; variants differ only in non-visual options (" + ", ".join(p.get("options", [])) + "), main product image used"
        elif vis:
            rec["v_withheld"] = ("Product has visual variants (" + ", ".join(p.get("options", [])) +
                                 ") and the source links no image to this SKU")
        else:
            rec["v_withheld"] = "Source product has no images"
        g = own + ([] if vis else unlinked)
        rec["g"] = [dict(url=u, page=p["url"], origin=p["source"]) for u in dict.fromkeys(g)
                    if u not in linked_other and (not rec["v"] or u != rec["v"]["url"])]
    if o.get("v") == "withhold":
        rec["v"] = None; rec["v_withheld"] = o.get("why", "withheld after visual review")
    elif o.get("v_url"):
        rec["v"] = dict(url=o["v_url"], page=o.get("page", rec["page"]), origin=o.get("origin", ""), kind="chosen at visual review")
        rec["note"] += "; " + o.get("why", "")
        rec["conf"] = o.get("conf", "Medium")
    if o.get("flag") and rec["v"]:
        rec["conf"] = "Medium"; rec["note"] += "; " + o["flag"]
    if o.get("drop_g"):
        rec["g"] = [g for g in rec["g"] if g["url"] not in set(o["drop_g"])]
    plan.append(rec)

print(brand, "rows", len(plan), Counter(bool(r["v"]) for r in plan), "matched", sum(1 for r in plan if r["resolution"]))

# ---------------------------------------------------------------- placeholders / non-product graphics
BAD_NAME = re.compile(config.get("bad_name_regex", r"placeholder|coming[-_ ]?soon|no[-_]?image|noimage|image[-_]not|"
                                               r"_ph[_.]|[-_]ph\.|award|badge|logo"), re.I)
PLACEHOLDERS = {imagehash.hex_to_hash(h) for h in json.load(open(WORK / "_all" / "placeholders.json"))}
for rec in plan:
    if rec["v"] and BAD_NAME.search(rec["v"]["url"].split("/")[-1]):
        rec["v_withheld"] = "source image is a placeholder/non-product graphic (" + rec["v"]["url"].split("/")[-1] + ")"
        rec["v"] = None
    rec["g"] = [g for g in rec["g"] if not BAD_NAME.search(g["url"].split("/")[-1])]

# ---------------------------------------------------------------- download
urls = [r["v"]["url"] for r in plan if r["v"]] + [g["url"] for r in plan for g in r["g"]]
paths = download_all(urls, W / "cache", workers=config.get("workers", 6), headers=config.get("download_headers"),
                     min_interval=config.get("min_interval", 0.15))
print("downloaded", sum(1 for u in set(urls) if paths.get(u)), "of", len(set(urls)))

# ---------------------------------------------------------------- process
cache = {}


def proc(u):
    if u not in cache:
        cache[u] = process_file(paths[u], u) if paths.get(u) else (None, dict(status="FAILED", why="download failed"))
    return cache[u]


bdir = brand_dir(brand)
results, written = [], {}
for rec in plan:
    d = OUT / list_dir(rec["list"]) / bdir; d.mkdir(parents=True, exist_ok=True)
    key = (rec["list"], rec["nsku"])
    if key in written:  # filename collision between two different list SKUs
        n = 2
        while (rec["list"], f"{rec['nsku']}__{n}") in written:
            n += 1
        rec["note"] += f"; filename collision with SKU '{written[key]}' - suffix __{n} added"
        rec["nsku"] = f"{rec['nsku']}__{n}"
    written[(rec["list"], rec["nsku"])] = rec["sku"]
    hashes = []
    if rec["v"]:
        data, info = proc(rec["v"]["url"])
        if data and any(imagehash.hex_to_hash(info["phash"]) - x <= 4 for x in PLACEHOLDERS):
            data, info = None, dict(status="FAILED", why="source image is a 'photo coming soon' placeholder")
        fn = f"{rec['nsku']}-V.jpg"
        if data:
            (d / fn).write_bytes(data); hashes.append(imagehash.hex_to_hash(info["phash"]))
        else:
            rec["v_withheld"] = "V image failed processing: " + info.get("why", "")
        results.append(dict(list=list_dir(rec["list"]), sku=rec["sku"], nsku=rec["nsku"], type="V", file=fn if data else "",
                            url=rec["v"]["url"], page=rec["v"]["page"], origin=rec["v"]["origin"], info=info))
    scored = []
    for order, g in enumerate(rec["g"]):
        if g["url"].lower().endswith(".gif"):
            continue
        data, info = proc(g["url"])
        if not data:
            continue
        h = imagehash.hex_to_hash(info["phash"])
        if any(h - x <= 4 for x in PLACEHOLDERS) or any(h - x <= 6 for x in hashes):
            continue
        hashes.append(h)
        scored.append((info["cls"], order, g, data, info))
    scored.sort(key=lambda t: (t[0], t[1]))
    for n, (_, _, g, data, info) in enumerate(scored[:config.get("max_g", MAX_G)], 1):
        fn = f"{rec['nsku']}-G-{n:02d}.jpg"
        (d / fn).write_bytes(data)
        results.append(dict(list=list_dir(rec["list"]), sku=rec["sku"], nsku=rec["nsku"], type="G", file=fn,
                            url=g["url"], page=g["page"], origin=g["origin"], info=info))

json.dump(results, open(W / "results.json", "w"), indent=1)
json.dump(plan, open(W / "plan_final.json", "w"), indent=1)
print("images", Counter((r["type"], r["info"]["status"]) for r in results))

# ---------------------------------------------------------------- visual QA sample sheet
V = [r for r in results if r["type"] == "V" and r["file"]]
random.seed(7)
samp = random.sample(V, min(60, len(V)))
if samp:
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 11)
    T, cols = 190, 6
    rows_n = (len(samp) + cols - 1) // cols
    sh = Image.new("RGB", (cols * T, rows_n * (T + 30)), "white"); dr = ImageDraw.Draw(sh)
    pl = {(r["list"], r["sku"]): r for r in plan}
    for k, r in enumerate(samp):
        x, y = (k % cols) * T, (k // cols) * (T + 30)
        sh.paste(Image.open(OUT / r["list"] / bdir / r["file"]).resize((T - 6, T - 6)), (x + 3, y + 3))
        dr.text((x + 3, y + T - 2), r["sku"][:30], fill="black", font=font)
        dr.text((x + 3, y + T + 12), pl[("List" + r["list"][-1], r["sku"])]["product"][:30], fill="gray", font=font)
    qa = Path("/tmp/claude-0/-home-user-lumera/fce5ed22-7126-5cd2-b6fe-945da1cbcd6a/scratchpad/qa"); qa.mkdir(parents=True, exist_ok=True)
    sh.save(qa / f"{slug(brand)}_V_sample.jpg", quality=72)
    print("QA sheet", qa / f"{slug(brand)}_V_sample.jpg")
