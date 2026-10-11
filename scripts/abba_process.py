"""Process planned images into 800x800 JPG <=100 KB, write per-list output, track state for resume.

Rules: keep aspect ratio (no crop, no distortion); pad to square with the image's own border colour
(median of the outer 2 px) so the original background is neither removed nor whitened; transparent
pixels (PNG cut-outs that have no background) are flattened onto white, recorded in Notes.
"""
import hashlib, io, json, re, sys
from pathlib import Path
import numpy as np, imagehash
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
W = ROOT / "work" / "abba"
OUT = ROOT / "Output"
BRAND_DIR = "ABBA_Lighting"
MAX_BYTES = 100_000          # 100 KB (decimal) - also below 100 KiB
SIDE = 800
MAX_G = 6                    # gallery cap per SKU
plan = json.load(open(W / "plan.json"))
index = json.load(open(W / "dl_index.json"))
OVR = json.load(open(W / "overrides.json")) if (W / "overrides.json").exists() else {}
# Per-image finish tags assigned at visual review (K black, W white, S stainless/silver/nickel, N natural brass,
# D dark brass, B brown/bronze, 0 finish-neutral drawing/spec, X unusable: mixed/unclear finish or other item).
TAGS = json.load(open(W / "finish_tags.json"))
CODE = {"Black": "K", "White": "W", "Stainless Steel": "S", "Silver": "S", "Nickel": "S",
        "Natural Brass": "N", "Dark Brass": "D", "Brown": "B"}

def norm_sku(s):
    s = s.replace("/", "-")
    s = re.sub(r"\s+", "", s)
    return re.sub(r'[<>:"\\|?*\x00-\x1f]', "", s)

def load(u):
    rec = index.get(u)
    if not rec or not rec.get("ok"):
        return None, "download failed"
    im = Image.open(W / "cache" / rec["file"])
    im.seek(0)
    return im, None

def flatten(im):
    note = ""
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        a = np.asarray(im)[:, :, 3]
        if a.min() < 250:
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[3])
            return bg, "transparent source flattened on white"
    return im.convert("RGB"), note

def border_colour(im):
    a = np.asarray(im)
    b = np.concatenate([a[:2].reshape(-1, 3), a[-2:].reshape(-1, 3), a[:, :2].reshape(-1, 3), a[:, -2:].reshape(-1, 3)])
    return tuple(int(x) for x in np.median(b, axis=0)), float(b.std(axis=0).mean())

def classify(im):
    """1 = white-background product shot, 2 = photographic/lifestyle, 3 = other (graphics, templates)."""
    a = np.asarray(im.resize((200, int(200 * im.height / im.width) or 1)))
    h, w = a.shape[:2]; k = max(2, int(min(h, w) * 0.06))
    frame = np.concatenate([a[:k].reshape(-1, 3), a[-k:].reshape(-1, 3), a[:, :k].reshape(-1, 3), a[:, -k:].reshape(-1, 3)])
    white = (frame.min(axis=1) > 232).mean()
    if white > 0.9:
        return 1
    return 2 if frame.std(axis=0).mean() > 25 else 3

def rgb2lab(a):
    a = a.astype(np.float64) / 255.0
    a = np.where(a > 0.04045, ((a + 0.055) / 1.055) ** 2.4, a / 12.92)
    xyz = a @ np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]]).T
    xyz /= np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)

def fg_stats(im):
    """Median Lab colour of the product (pixels that differ from a uniform border), foreground share,
    whether the background is uniform, and whether the image is a line drawing (finish-neutral)."""
    t = im.copy(); t.thumbnail((160, 160))
    a = np.asarray(t).astype(np.int16)
    col, std = border_colour(t)
    d = np.sqrt(((a - np.array(col)) ** 2).sum(-1))
    fg = d > 45
    frac = float(fg.mean())
    uniform = std < 18
    lab = np.median(rgb2lab(a[fg].astype(np.uint8)), axis=0).tolist() if fg.sum() > 30 else None
    drawing = uniform and min(col) > 225 and frac < 0.10
    return dict(lab=lab, frac=frac, uniform=uniform, drawing=drawing)

def delta_e(a, b):
    return float(np.sqrt(sum((x - y) ** 2 for x, y in zip(a, b))))

def to_square(im):
    w, h = im.size
    scale = min(SIDE / w, SIDE / h)
    nw, nh = max(1, round(w * scale)), max(1, round(h * scale))
    rs = im.resize((nw, nh), Image.LANCZOS) if (nw, nh) != (w, h) else im
    col, _ = border_colour(im)
    can = Image.new("RGB", (SIDE, SIDE), col)
    can.paste(rs, ((SIDE - nw) // 2, (SIDE - nh) // 2))
    return can, scale

def encode(im):
    for sub, qs in ((0, range(95, 79, -3)), (2, range(90, 39, -4))):
        for q in qs:
            b = io.BytesIO(); im.save(b, "JPEG", quality=q, subsampling=sub, optimize=True, progressive=True)
            if b.tell() <= MAX_BYTES:
                return b.getvalue(), q, sub
    return None, None, None

def process(u):
    im, err = load(u)
    if err:
        return None, dict(status="FAILED", why=err)
    src_px = im.size
    im, tnote = flatten(im)
    if max(src_px) < 400:
        return None, dict(status="FAILED", why=f"source only {src_px[0]}x{src_px[1]} px (too small; would need >2x upscale)", src_px=src_px)
    cls = classify(im)
    ph = imagehash.phash(im)
    sq, scale = to_square(im)
    data, q, sub = encode(sq)
    if data is None:
        return None, dict(status="FAILED", why="cannot reach <=100 KB at JPEG quality >=40", src_px=src_px)
    notes = [n for n in (tnote,) if n]
    if scale > 1.0:
        notes.append(f"upscaled x{scale:.2f} from {src_px[0]}x{src_px[1]} (best verified source available)")
    if src_px[0] != src_px[1]:
        notes.append(f"padded from {src_px[0]}x{src_px[1]} aspect")
    if q < 60:
        notes.append(f"low JPEG quality {q} needed for 100 KB limit")
    if Path(u).suffix.lower() == ".gif":
        notes.append("first frame of animated GIF")
    return data, dict(status="OK", cls=cls, phash=str(ph), fg=fg_stats(im), q=q, sub=sub, src_px=src_px, scale=scale, notes=notes)

cache = {}
def proc_cached(u):
    if u not in cache:
        cache[u] = process(u)
    return cache[u]

results = []
written = set()
for rec in plan:
    o = OVR.get(rec["sku"], {})
    if o.get("v") == "withhold":
        rec["v_withheld"] = o.get("why", "withheld after visual review"); rec["v"] = None
    elif o.get("v_url"):
        rec["v"] = dict(url=o["v_url"], page=o.get("page", rec["page"]), origin=o.get("origin", "abbalightingusa.com"), kind="official image chosen at visual review")
        rec["note"] += "; " + o.get("why", "")
    drop = set(o.get("drop_g", []))
    lst = "List_" + rec["list"].replace("List", "")
    d = OUT / lst / BRAND_DIR; d.mkdir(parents=True, exist_ok=True)
    nsku = norm_sku(rec["sku"])
    rec["nsku"] = nsku
    vhash = None
    if rec["v"]:
        data, info = proc_cached(rec["v"]["url"])
        fn = f"{nsku}-V.jpg"
        if data:
            p = d / fn
            assert str(p) not in written, f"filename collision {p}"
            p.write_bytes(data); written.add(str(p))
            vhash = imagehash.hex_to_hash(info["phash"])
        results.append(dict(rec=rec, type="V", file=fn if data else "", src=rec["v"], info=info, list=lst))
    hashes = [vhash] if vhash else []
    finish_specific = bool(rec.get("finish"))
    rec["g_rejected_finish"] = []
    picked = []
    cands = [g for g in rec["g"] if not g.get("excluded") and g["url"] not in drop]
    scored = []
    for order, g in enumerate(cands):
        data, info = proc_cached(g["url"])
        if not data:
            continue
        if Path(g["url"]).suffix.lower() == ".gif":
            continue  # animated GIFs are not used as gallery stills
        if finish_specific:
            # Product is sold in several finishes: keep only images visually tagged with this SKU's finish
            # (or finish-neutral drawings).
            t = TAGS.get(rec["product"], {}).get(g["url"], "X")
            if t not in (CODE[rec["finish"]], "0"):
                rec["g_rejected_finish"].append(g["url"]); continue
        h = imagehash.hex_to_hash(info["phash"])
        if any(h - x <= 6 for x in hashes):
            continue  # duplicate / near-duplicate of V or an earlier G
        hashes.append(h)
        scored.append((info["cls"], order, g, data, info))
    scored.sort(key=lambda t: (t[0], t[1]))
    for n, (cls, _, g, data, info) in enumerate(scored[:MAX_G], 1):
        fn = f"{nsku}-G-{n:02d}.jpg"
        p = d / fn
        assert str(p) not in written, f"filename collision {p}"
        p.write_bytes(data); written.add(str(p))
        results.append(dict(rec=rec, type="G", file=fn, src=g, info=info, list=lst))
    rec["g_used"] = min(len(scored), MAX_G)
    rec["g_available"] = len(scored)

json.dump([dict(list=r["list"], sku=r["rec"]["sku"], nsku=r["rec"]["nsku"], type=r["type"], file=r["file"], url=r["src"]["url"],
                page=r["src"]["page"], origin=r["src"]["origin"], info=r["info"]) for r in results],
          open(W / "results.json", "w"), indent=1)
json.dump(plan, open(W / "plan_final.json", "w"), indent=1)
from collections import Counter
print("images", Counter((r["type"], r["info"]["status"]) for r in results), "files", len(written))
