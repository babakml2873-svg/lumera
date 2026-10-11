"""Build the per-SKU image plan for brand ABBA Lighting.

Inputs : product list CSV (argv[1]); cached official catalog work/abba/store_all.json + var/*.json
         (WooCommerce Store API of www.abbalightingusa.com = ABBA Lighting USA, official US distributor);
         cached reseller product JSON in work/abba/retail/ (only for SKUs the official site no longer lists).
Output : work/abba/plan.json  - one record per list row with resolved product, confidence, V source and G candidates.
Lumera Electric is never used as a source (asserted for every URL).
"""
import csv, glob, html, json, re, sys
from pathlib import Path

W = Path(__file__).resolve().parent.parent / "work" / "abba"
SITE = "https://www.abbalightingusa.com"
ps = {p["id"]: p for p in json.load(open(W / "store_all.json"))}
vs = {v["id"]: v for v in (json.load(open(f)) for f in glob.glob(str(W / "var" / "*.json")))}
norm = lambda s: re.sub(r"[^A-Z0-9]", "", s.upper())

def origin(src):
    u = re.sub(r"^https://i\d\.wp\.com/", "https://", src.split("?")[0])
    assert "lumera" not in u.lower(), u
    return u

def retail(fn):
    p = json.load(open(W / "retail" / fn))["product"]
    dom = fn.split("__")[0]
    return p, f"https://{dom}/products/{p['handle']}"

# ---------------------------------------------------------------- resolution tables
# Exact list-SKU string -> resolution when the list SKU is not literally an official SKU.
# (kind, id, confidence, note). kind V = official variation, P = official simple product.
MANUAL = {
    "MR16 3W-27K": ("V", 6275, "Medium", "Official variation Color Temperature 2700K (site labels it SKU MR16-3W-3K); all CCT variants share one fixture image"),
    "STS600-2 ZONE": ("P", 9309, "High", "Official SKU 'STS600-2 (2-Zone)'"),
    "STS300-2 ZONE": ("P", 9307, "High", "Official SKU 'STS300-2 (2-Zone)'"),
    "TSDLCD 24100": ("P", 12129, "High", "Official product TSDLCD24100"),
    "TSDLCD 12100": ("P", 12127, "High", "Official product TSDLCD12100"),
    "TSDCT 24100": ("P", 12126, "High", "Official product TSDCT24100"),
    "TSDCT 12100": ("P", 12124, "High", "Official product TSDCT12100"),
    "MX24150": ("P", 10370, "High", "Official product MX24150-DC TRANSFORMER"),
    "CCDA95": ("P", 5558, "High", "Official product CCDA95"),
    "PLB29": ("P", 9396, "High", "Official product PLB29-BRASS PATH LIGHT"),
    "CDPA78": ("P", 12018, "High", "Official product CDPA78"),
    "CDPA77": ("P", 12015, "High", "Official product CDPA77"),
    "CDPA73": ("P", 7832, "High", "Official product CDPA73"),
    "CDPA70": ("P", 7667, "High", "Official product CDPA70"),
    "CDPA69": ("P", 39265, "High", "Official product CDPA69"),
    "CDPA56": ("P", 2931, "High", "Official product CDPA56 (site SKU CD56)"),
    "CDPA54": ("P", 4218, "High", "Official product CDPA54"),
    "TM02": ("P", 20577, "High", "Official product TM02-MECHANICAL TIMER"),
    "TM01": ("P", 20571, "High", "Official product TM01-MECHANICAL TIMER"),
    "SLGC111": ("P", 9036, "High", "Official product SLGC111"),
    "SLGC55": ("P", 9008, "High", "Official product SLGC55"),
    "PS1": ("P", 3303, "High", "Official product PS1 - ABS PLASTIC SPIKE"),
    "DMX31": ("P", 5371, "High", "Official product DMX31"),
    "AC/DC": ("P", 7485, "Medium", "Official product 'AC DC CONNECTOR' (site SKU is a UPC)"),
    "CRG31-RGBW": ("P", 6029, "High", "Official product CRG31-RGBW BRICK LIGHT"),
    "CRG30-RGBW": ("P", 2420, "High", "Official product CRG30-RGBW BRICK LIGHT"),
    "CRG30-WW": ("P", 6026, "High", "Official product CRG30-WARM WHITE BRICK LIGHT"),
    "FLACCT 40-3CCT": ("P", 9041, "High", "Official product FLACCT40 (3CCT)"),
    "FLACCT 20-3CCT": ("P", 7633, "High", "Official product FLACCT20 (3CCT)"),
    "STS Blank": ("P", 10274, "High", "Official product STSB-BLANK MODULE"),
    "STSWIFI": ("P", 5468, "Medium", "Official product STSW-WIFI module"),
    "STSLCD": ("P", 10270, "Medium", "Official product STSTLCD-Astronomic Timer (STS LCD module)"),
    "STB06-3K": ("P", 3145, "Medium", "Official product STB06 (single listing, no CCT options)"),
    "STB05-3K": ("P", 3152, "Medium", "Official product STB05 (single listing, no CCT options)"),
    "STB05R-27K": ("P", 8226, "Medium", "Official product STB05R (single listing, no CCT options)"),
    "CDPAR60-RGBW": ("P", 9187, "Medium", "Official product CDPAR60-RGBCW (site SKU CDPAR60)"),
    "DLO3-Br": ("V", 4154, "Medium", "List SKU contains letter O; official DL03-Br [Finish: Brown]"),
    "CD75-Bk 4K": ("V", 8255, "Medium", "Official variation Black/4000K; its own image is an accessories shot, so the Black fixture image of official variation CD75-BLK-3K is used"),
    "CD75-Bk 5K": ("V", 8257, "Medium", "Official variation Finish Black/5000K (site SKU mislabeled CD75-BR-5K)"),
    "MR16-Blue": ("V", 4204, "Medium", "Official variation attribute Blue with image MR16-Blue (site SKU mislabeled MR16-Red)"),
    "MR16-Red": ("V", 4206, "Medium", "Official variation attribute Red with image MR16-Red (site SKU mislabeled MR11-Red); site SKU 'MR16-Red' shows the BLUE bulb, so it was not used"),
    "STA10-Bz": ("V", 8327, "Medium", "List code Bz = official Brown finish (reseller Kings Outdoor Lighting sells STA10BZ 'Dark Bronze' with the official STA10 BROWN image)"),
    "STA11-Bz": ("V", 8329, "Medium", "List code Bz = official Brown finish (reseller Kings Outdoor Lighting sells STA11BZ 'Dark Bronze' with the official STA11 BROWN image)"),
    "CB04-S": ("V", 5259, "Medium", "List code S = official Nickel finish (official image file is named cb04-silver; resellers list it as Nickel / Brushed Nickel)"),
}
V_IMG_FROM = {"CD75-Bk 4K": 8253}
V_IMG_URL = {  # explicit official V image when the variation image itself is unsuitable
    "STA10-Bz": None,  # filled below from the official parent gallery (BROWN template)
}
SS_NOTE = ("List code SS mapped to official Silver finish (ABBA resellers use SS = Silver on these puck lights: "
           "Sonic Electric CB07-SS-30K = Silver, Kings Outdoor Lighting CB07SS = Silver)")
ATTR_RULES = {  # list SKU -> (parent, finish, cct-or-exact-attr, confidence, extra note)
    "E26 4W-5K": (3209, None, "5000K"), "E26 4W-3K": (3209, None, "3000K"),
    "E12 4W-5K": (5729, None, "5000K"), "E12 4W-3K": (5729, None, "3000K"),
    "E12 3W-5K": (3213, None, "5000K"), "E12 3W-3K": (3213, None, "3000K"),
    "CD75-Bk 3K": (2680, "Black", "3000K"),
    "CD20-Bk 5K": (2766, None, "5000K", "Medium", "CD20 is sold in a single (black) finish"),
    "CD20-Bk 3K": (2766, None, "3000K", "Medium", "CD20 is sold in a single (black) finish"),
    "BRT1-DB": (24786, "Dark Brass", None), "BRT1-NB": (24786, "Natural Brass", None),
    "BRL2-DB": (24916, "Dark Brass", None), "BRL2-NB": (24916, "Natural Brass", None),
    "BA15S-5W 5K": (4867, None, "5000K"), "BA15S-5W 3K": (4867, None, "3000K"),
    "BA15D-3.5W 5K": (5506, None, "5000K"), "BA15D-3.5W 3K": (5506, None, "3000K"),
    "CDPA50-Bk": (5234, "Black", None), "CDPA57-Bk": (2872, "Black", None),
    "CDPA65-Bk": (2889, "Black", None), "CDPA71-Bk": (9218, "Black", None),
    "CDPA71-Wh": (9218, "White", None), "CDPS59-Bk": (2960, "Black", None),
    "CB04-Bk": (5060, "Black", None), "CD43-Bk": (1955, "Black", None), "DL01-Bk": (2646, "Black", None),
}
for model, par in (("PL54", 5538), ("PL15", 5519)):
    for ln in ("150", "100", "50"):
        ATTR_RULES[f"{model} RGBW {ln}F"] = (par, None, f"={ln}ft")
for model, par in (("PL54", 5934), ("PL15", 5935)):
    for ln in ("150", "100", "50", "5"):
        ATTR_RULES[f"{model} RGB {ln}F"] = (par, None, f"={ln}ft")
for f, par in (("CB15", 2189), ("CB07", 3669), ("CB06", 2200), ("CB05", 2221)):
    for k in ("3K", "5K"):
        ATTR_RULES[f"{f}-Bk {k}"] = (par, "Black", k[0] + "000K")
        ATTR_RULES[f"{f}-SS {k}"] = (par, "Silver", k[0] + "000K", "Medium", SS_NOTE)

# Products the official site no longer lists; exact variant SKU found at an ABBA reseller.
RETAIL = {
    "STB18-DB": ("sonicelectric.com__abba-stb18-integrated-3w-12v-brass-led-step-light.json", "STB18-DB"),
    "STB18-NB": ("sonicelectric.com__abba-stb18-integrated-3w-12v-brass-led-step-light.json", "STB18-NB"),
    "CDPSR59-SS": ("kingsoutdoorlighting.com__cdpsr59-wifi-smart-rgbcw-3w-stainless-steel-directional-pathway-light-led-bollard-landscape-lighting-copy.json", "CDPSR59-SS"),
}
RETAIL_GALLERY_PARENT = {"CDPSR59-SS": 8690}  # official gallery still exists for this model

REVIEW = {
    "SL102-RGB": "Model SL102 RGB not found on the official site or ABBA resellers (SL102 results are other brands)",
    "BP1-Wh": "BP1 is offered only in Natural Brass / Dark Brass (official site and resellers); no White variant",
    "STB19-Bz": "STB19 is offered in Black / White / Natural Brass only; no Bronze variant found",
    "E27-RGB": "Only an 'E27 6W RGBW/RGBCW' exists officially/at resellers; RGB vs RGBW identity not confirmed",
    "SL101-3K": "Ambiguous: SL101 bistro string light (Black/White, 3000K) vs SL101-LB2W 3K replacement bulb",
    "PLB01-DB": "Official PLB01 is one listing without finish options; a Dark Brass variant SKU could not be confirmed",
    "CDPA52-Bk": "Official CDPA52 is one listing without finish options; Black variant image not identifiable",
    "CDPA52-Br": "Official CDPA52 is one listing without finish options; Brown/Bronze variant image not identifiable",
}

# ---------------------------------------------------------------- helpers
def attrs(v):
    return [b.strip(" :") for _, b in (x.split(":", 1) for x in re.split(r",\s*(?=[A-Za-z ]+:)", v["variation"]))]

def by_attr(parent, finish, cct):
    out = []
    for v in vs.values():
        if v["parent"] != parent:
            continue
        a = [x.lower() for x in attrs(v)]
        if finish and finish.lower() not in a:
            continue
        if cct and cct.startswith("="):
            if not any(x.replace(" ", "").replace(".", "") == cct[1:] for x in a):
                continue
        elif cct and cct.lower() not in a:
            continue
        out.append(v["id"])
    return out

FIN_TOK = {"Black": {"BLACK", "BK", "BLK", "B"}, "Brown": {"BROWN", "BR", "BRWN", "BZ", "BRONZE"},
           "White": {"WHITE", "WH", "WHT", "W"}, "Silver": {"SILVER", "SL", "SLV", "SIL"},
           "Stainless Steel": {"SS", "STAINLESS"}, "Natural Brass": {"NB", "NATURAL"},
           "Dark Brass": {"DB", "DARK", "BRONZE"}, "Nickel": {"NK", "NICKEL", "BN", "SILVER"}}
LIST_FIN = {"BK": "Black", "BLK": "Black", "BR": "Brown", "BZ": "Brown", "SS": "Stainless Steel",
            "WH": "White", "NB": "Natural Brass", "DB": "Dark Brass", "S": "Nickel"}

def sku_finish(sku, chosen_variation=None):
    if chosen_variation:
        for a in attrs(chosen_variation):
            if a in FIN_TOK:
                return a
    for t in re.split(r"[- ]", sku.upper())[1:]:
        if t in LIST_FIN:
            return LIST_FIN[t]
    return None

def sku_cct(sku):
    m = re.search(r"(?<![0-9])(27|3|4|5)K\b", sku.upper())
    return {"27": "2700K", "3": "3000K", "4": "4000K", "5": "5000K"}[m.group(1)] if m else None

MODEL_RE = re.compile(r"([A-Z]{1,6})(\d{2,5})")

def model_of(name):
    m = MODEL_RE.search(html.unescape(name).upper())
    return m.groups() if m else None

def foreign_model(fname, model):
    """True if the filename names a different product model (e.g. DM52 slide on the UNB06 page)."""
    if not model:
        return False
    pre, dig = model
    toks = MODEL_RE.findall(re.sub(r"[^A-Z0-9]", " ", fname.upper().replace("RGBCW", " ")))
    toks = [(a, b) for a, b in toks if len(a) >= 2 and a not in {"JPG", "PNG", "PM", "AM", "FILE", "X", "HD", "TV", "LED", "AI", "P", "NEW", "IMG", "BG"}]
    if not toks:
        return False
    def subseq(a, b):
        it = iter(b); return all(c in it for c in a)
    for a, b in toks:
        if b.lstrip("0") == dig.lstrip("0") and (a[:2] == pre[:2] or subseq(a, pre)):
            return False
    return True

def conflicting_finish(fname, finish):
    if not finish:
        return False
    toks = set(re.split(r"[^A-Z]+", fname.upper()))
    mine = FIN_TOK.get(finish, set())
    for other, tk in FIN_TOK.items():
        if other == finish:
            continue
        hit = (tk - {"B", "W"}) & toks
        if hit and not (mine & toks):
            return True
    return False

def conflicting_cct(fname, cct):
    if not cct:
        return False
    found = set(re.findall(r"(2700|3000|4000|5000)K", fname.upper()))
    return bool(found) and cct[:4] not in found

# ---------------------------------------------------------------- build plan
rows = [r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")) if r["Brand"] == "ABBA Lighting"]
plan = []
for r in rows:
    s = r["SKU"]
    rec = dict(list=r["List"], brand=r["Brand"], sku=s, resolution="", product="", page="", conf="", note="",
               review="", v=None, g=[])
    var = None; pid = None
    if s in REVIEW:
        rec["review"] = REVIEW[s]
    elif s in RETAIL:
        fn, vsku = RETAIL[s]
        p, page = retail(fn)
        v = next(v for v in p["variants"] if v["sku"] == vsku)
        img = next((i for i in p["images"] if i["id"] == v.get("image_id")), None)
        rec["finish"] = sku_finish(s)
        rec.update(resolution="reseller-exact-variant-SKU", product=p["title"], page=page + f"?variant={v['id']}",
                   conf="High", note=f"Not listed on official site; exact variant SKU '{vsku}' [{v['title']}] at ABBA reseller {fn.split('__')[0]}")
        if img:
            rec["v"] = dict(url=img["src"].split("?")[0], page=rec["page"], origin=fn.split("__")[0], kind="variant image linked to SKU")
        if s in RETAIL_GALLERY_PARENT:
            pid = RETAIL_GALLERY_PARENT[s]
        else:
            fin = sku_finish(s)
            for i in p["images"]:
                u = i["src"].split("?")[0]
                if rec["v"] and u == rec["v"]["url"]:
                    continue
                if i.get("variant_ids"):
                    continue  # image tied to another variant (other finish)
                rec["g"].append(dict(url=u, page=page, origin=fn.split("__")[0], w=i["width"], h=i["height"]))
    else:
        hit = None
        if s in MANUAL:
            k, i, c, n = MANUAL[s]
            hit = (k, i); rec.update(conf=c, note=n)
        elif s in ATTR_RULES:
            rule = ATTR_RULES[s]
            parent, fin, cct = rule[:3]
            ids = by_attr(parent, fin, cct)
            if len(ids) == 1:
                hit = ("V", ids[0])
                v = vs[ids[0]]
                rec.update(conf=rule[3] if len(rule) > 3 else "High",
                           note=(rule[4] + "; " if len(rule) > 4 else "") +
                           f"Attribute match on official variation [{v['variation']}] (site SKU '{v['sku']}')")
            else:
                rec["review"] = f"Attribute lookup returned {len(ids)} variations"
        else:
            h = skuidx = None
            idx = {}
            for p in ps.values():
                if p["sku"]: idx.setdefault(norm(p["sku"]), []).append(("P", p["id"]))
            for v in vs.values():
                if v["sku"]: idx.setdefault(norm(v["sku"]), []).append(("V", v["id"]))
            h = idx.get(norm(s), [])
            if len(h) == 1:
                hit = h[0]
                k, i = hit
                rec.update(conf="High", note=(f"Exact official variation SKU '{vs[i]['sku']}' [{vs[i]['variation']}]" if k == "V"
                                              else f"Exact official product SKU '{ps[i]['sku']}'"))
            else:
                rec["review"] = f"{len(h)} official SKU matches"
        if hit:
            k, i = hit
            if k == "V":
                var = vs[i]; pid = var["parent"]
                rec.update(resolution="official-variation", page=var["permalink"])
                vsrc = vs[V_IMG_FROM.get(s, i)]
                if vsrc["images"]:
                    rec["v"] = dict(url=origin(vsrc["images"][0]["src"]), page=vsrc["permalink"], origin="abbalightingusa.com",
                                    kind="official variation image")
            else:
                pid = i
                rec.update(resolution="official-product", page=ps[i]["permalink"])
            rec["product"] = html.unescape(ps[pid]["name"])
    # official gallery candidates (with filters)
    if pid:
        p = ps[pid]
        model = model_of(p["name"])
        fin = sku_finish(s, var) if (var or rec["resolution"].startswith("reseller")) else None
        if rec["resolution"].startswith("reseller"):
            fin = sku_finish(s)
        cct = sku_cct(s) if var else None
        imgs = p["images"]
        if rec["resolution"] == "official-product" and not rec["v"] and imgs:
            rec["v"] = dict(url=origin(imgs[0]["src"]), page=p["permalink"], origin="abbalightingusa.com",
                            kind="official product main image")
        for im in imgs:
            u = origin(im["src"]); fn = Path(u).name
            reason = None
            if rec["v"] and u == rec["v"]["url"]:
                continue
            if foreign_model(fn, model): reason = "other model in filename"
            elif conflicting_cct(fn, cct): reason = f"other CCT than {cct}"
            rec["g"].append(dict(url=u, page=p["permalink"], origin="abbalightingusa.com", excluded=reason,
                                 name_finish_conflict=conflicting_finish(fn, fin)))
        rec["finish"] = fin; rec["cct"] = cct; rec["model"] = "".join(model) if model else ""
    plan.append(rec)

# STA10-Bz: variation image is a generic shot; use the official BROWN template from the STA10 gallery instead
for rec in plan:
    if rec["sku"] == "STA10-Bz":
        brown = [g for g in rec["g"] if "BROWN" in g["url"].upper()]
        if brown:
            rec["v"] = dict(url=brown[0]["url"], page=rec["page"], origin="abbalightingusa.com", kind="official gallery image (Brown finish)")
            rec["g"] = [g for g in rec["g"] if g["url"] != brown[0]["url"]]

# V sanity: an official image whose filename names another model or another finish is not accepted as V.
for rec in plan:
    v = rec["v"]
    if not v or v["origin"] != "abbalightingusa.com" or not rec.get("model"):
        continue
    fn = Path(v["url"]).name
    model = MODEL_RE.search(rec["model"]).groups()
    bad = ("names another model" if foreign_model(fn, model) else
           f"shows another finish than {rec['finish']}" if conflicting_finish(fn, rec["finish"]) else None)
    if not bad:
        continue
    fintok = FIN_TOK.get(rec["finish"], set()) - {"B", "W"}
    alt = None
    for g in rec["g"]:
        gfn = Path(g["url"]).name.upper()
        if g.get("excluded") or foreign_model(gfn, model) or not MODEL_RE.search(gfn) \
                or model[1] not in [d for _, d in MODEL_RE.findall(re.sub(r"[^A-Z0-9]", " ", gfn))]:
            continue
        if Path(gfn).suffix == ".GIF":
            continue
        if rec["finish"] is None or rec["resolution"] == "official-product" or (fintok & set(re.split(r"[^A-Z]+", gfn))):
            alt = g; break
    old = Path(v["url"]).name
    if alt:
        rec["v"] = dict(url=alt["url"], page=alt["page"], origin=alt["origin"], kind="official gallery image (replacement)")
        rec["g"] = [g for g in rec["g"] if g["url"] != alt["url"]]
        rec["note"] += f"; official variant image '{old}' {bad}, replaced by official '{Path(alt['url']).name}'"
        if rec["conf"] == "High":
            rec["conf"] = "Medium"
    else:
        rec["v"] = None
        rec["v_withheld"] = f"Official variant image '{old}' {bad}; no official image of {rec['model']} in this finish found"

json.dump(plan, open(W / "plan.json", "w"), indent=1)
for rec in plan:
    if "replaced by" in rec["note"] or rec.get("v_withheld"):
        print(" *", rec["sku"], "|", rec.get("v_withheld") or rec["note"].split("; ")[-1])
from collections import Counter
print("rows", len(plan), Counter(r["resolution"] or "REVIEW" for r in plan), Counter(r["conf"] for r in plan))
print("with V src", sum(1 for r in plan if r["v"]), "G candidates", sum(len([g for g in r["g"] if not g.get("excluded")]) for r in plan),
      "excluded", Counter(g["excluded"].split(" than")[0] for r in plan for g in r["g"] if g.get("excluded")))
