"""Shared helpers for the brand-by-brand product image pipeline.

Rules implemented here (same as the first brand, ABBA Lighting):
  * 800x800 JPG, <= 100,000 bytes, aspect ratio kept, no crop, no distortion
  * padding uses the image's own border colour (backgrounds are never removed or whitened);
    transparent cut-outs (no background) are flattened on white and noted
  * sources from Lumera Electric are rejected everywhere
"""
import csv, hashlib, io, json, re, threading, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

import imagehash
import numpy as np
import requests
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
WORK = ROOT / "work"
OUT = ROOT / "Output"
SRC_CSV = "/root/.claude/uploads/fce5ed22-7126-5cd2-b6fe-945da1cbcd6a/1f8d562c-report_images.csv"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
HEADERS = {"User-Agent": UA, "Accept": "text/html,application/json;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.9"}
SIDE = 800
MAX_BYTES = 100_000
MAX_Q = 88          # quality ceiling keeps files small without visible loss
MAX_G = 4           # gallery cap per SKU (reduced from 6 after the first brand, for repository size)
BANNED = ("lumera",)


def slug(brand):
    return re.sub(r"[^A-Za-z0-9]+", "_", brand).strip("_")


def brand_dir(brand):
    return slug(brand)


def match_key(s):
    """Key used to compare a list SKU with a source SKU (case/punctuation-insensitive)."""
    s = s.strip().lstrip("'").strip()
    return re.sub(r"[^A-Z0-9]", "", s.upper())


def file_sku(s):
    """Filename form of a SKU per the brief: '/' -> '-', spaces and prohibited characters removed."""
    s = s.strip().lstrip("'").strip()
    s = s.replace("/", "-")
    s = re.sub(r"\s+", "", s)
    return re.sub(r'[<>:"\\|?*\x00-\x1f\']', "", s)


def list_dir(lst):
    return "List_" + lst.replace("List", "")


def load_rows(brand):
    return [r for r in csv.DictReader(open(SRC_CSV, encoding="utf-8")) if r["Brand"] == brand]


def assert_allowed(url):
    low = url.lower()
    assert not any(b in low for b in BANNED), f"banned source: {url}"
    return url


# ------------------------------------------------------------------ HTTP
_host_lock = {}
_host_last = {}


def get(url, as_json=False, timeout=60, retries=3, min_interval=0.4, headers=None):
    assert_allowed(url)
    host = urlparse(url).netloc
    lock = _host_lock.setdefault(host, threading.Lock())
    err = None
    for attempt in range(retries):
        with lock:
            wait = _host_last.get(host, 0) + min_interval - time.time()
            if wait > 0:
                time.sleep(wait)
            _host_last[host] = time.time()
        try:
            r = requests.get(url, headers={**HEADERS, **(headers or {})}, timeout=timeout)
            if r.status_code == 429 or r.status_code >= 500:
                err = f"HTTP {r.status_code}"
                time.sleep(5 * (attempt + 1))
                continue
            if as_json:
                return r.status_code, (r.json() if r.status_code == 200 else None), r.headers
            return r.status_code, r.content, r.headers
        except Exception as e:  # network hiccup -> retry
            err = str(e)
            time.sleep(3 * (attempt + 1))
    return None, None, {"error": err}


def download_all(urls, cache_dir, workers=6):
    """Download each URL once into cache_dir; returns {url: path or None}. Resumable via index.json."""
    cache_dir = Path(cache_dir); cache_dir.mkdir(parents=True, exist_ok=True)
    idx_p = cache_dir / "index.json"
    index = json.load(open(idx_p)) if idx_p.exists() else {}
    todo = [u for u in dict.fromkeys(urls) if not (index.get(u) and (cache_dir / index[u]).exists())]

    def one(u):
        ext = (Path(urlparse(u).path).suffix.lower() or ".img")[:6]
        fn = hashlib.sha1(u.encode()).hexdigest()[:20] + ext
        code, data, hdr = get(u, timeout=90, min_interval=0.15)
        ok = code == 200 and data and len(data) > 500 and not data[:15].lstrip().lower().startswith((b"<!doc", b"<html"))
        if ok:
            (cache_dir / fn).write_bytes(data)
        return u, fn if ok else None

    with ThreadPoolExecutor(workers) as ex:
        for n, (u, fn) in enumerate(ex.map(one, todo)):
            index[u] = fn
            if n % 200 == 0:
                json.dump(index, open(idx_p, "w"))
    json.dump(index, open(idx_p, "w"))
    return {u: (cache_dir / index[u]) if index.get(u) else None for u in urls}


# ------------------------------------------------------------------ image processing
def flatten(im):
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        if np.asarray(im)[:, :, 3].min() < 250:
            bg = Image.new("RGB", im.size, (255, 255, 255))
            bg.paste(im, mask=im.split()[3])
            return bg, "transparent source flattened on white"
    return im.convert("RGB"), ""


def border_colour(im):
    a = np.asarray(im)
    b = np.concatenate([a[:2].reshape(-1, 3), a[-2:].reshape(-1, 3), a[:, :2].reshape(-1, 3), a[:, -2:].reshape(-1, 3)])
    return tuple(int(x) for x in np.median(b, axis=0)), float(b.std(axis=0).mean())


def classify(im):
    """1 = white-background product shot, 2 = photographic/lifestyle, 3 = other (graphics/templates)."""
    t = im.copy(); t.thumbnail((200, 200))
    a = np.asarray(t)
    h, w = a.shape[:2]; k = max(2, int(min(h, w) * 0.06))
    frame = np.concatenate([a[:k].reshape(-1, 3), a[-k:].reshape(-1, 3), a[:, :k].reshape(-1, 3), a[:, -k:].reshape(-1, 3)])
    if (frame.min(axis=1) > 232).mean() > 0.9:
        return 1
    return 2 if frame.std(axis=0).mean() > 25 else 3


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
    for sub, qs in ((0, range(MAX_Q, 79, -3)), (2, range(min(MAX_Q, 88), 39, -4))):
        for q in qs:
            b = io.BytesIO(); im.save(b, "JPEG", quality=q, subsampling=sub, optimize=True, progressive=True)
            if b.tell() <= MAX_BYTES:
                return b.getvalue(), q
    return None, None


def process_file(path, src_url=""):
    """Returns (jpeg_bytes or None, info dict)."""
    try:
        im = Image.open(path); im.seek(0); im.load()
    except Exception as e:
        return None, dict(status="FAILED", why=f"unreadable image ({e.__class__.__name__})")
    src_px = im.size
    im, tnote = flatten(im)
    if max(src_px) < 400:
        return None, dict(status="FAILED", why=f"source only {src_px[0]}x{src_px[1]} px (too small)", src_px=src_px)
    cls = classify(im)
    ph = str(imagehash.phash(im))
    sq, scale = to_square(im)
    data, q = encode(sq)
    if data is None:
        return None, dict(status="FAILED", why="cannot reach <=100 KB at JPEG quality >=40", src_px=src_px)
    notes = [n for n in (tnote,) if n]
    if scale > 1.0:
        notes.append(f"upscaled x{scale:.2f} from {src_px[0]}x{src_px[1]} (best verified source available)")
    if src_px[0] != src_px[1]:
        notes.append(f"padded from {src_px[0]}x{src_px[1]} aspect")
    if q < 60:
        notes.append(f"low JPEG quality {q} needed for 100 KB limit")
    if src_url.lower().split("?")[0].endswith(".gif"):
        notes.append("first frame of animated GIF")
    return data, dict(status="OK", cls=cls, phash=ph, q=q, src_px=list(src_px), scale=scale, notes=notes)
