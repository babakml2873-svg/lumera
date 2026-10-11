"""Download (cache + resume) every image referenced by work/abba/plan.json.
Allowed origins: www.abbalightingusa.com (official) and cdn.shopify.com files of the named ABBA resellers.
Lumera Electric domains/CDN are rejected."""
import hashlib, json, subprocess, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
W = Path(__file__).resolve().parent.parent / "work" / "abba"
C = W / "cache"; C.mkdir(exist_ok=True)
plan = json.load(open(W / "plan.json"))
ALLOWED = ("https://www.abbalightingusa.com/wp-content/uploads/", "https://cdn.shopify.com/s/files/")
urls = set()
for r in plan:
    for x in ([r["v"]] if r["v"] else []) + [g for g in r["g"] if not g.get("excluded")]:
        u = x["url"]
        assert u.startswith(ALLOWED) and "lumera" not in u.lower(), u
        urls.add(u)
IDX = W / "dl_index.json"
index = json.load(open(IDX)) if IDX.exists() else {}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"
def fetch(u):
    ext = Path(u).suffix.lower() or ".bin"
    fn = C / (hashlib.sha1(u.encode()).hexdigest()[:16] + ext)
    if fn.exists() and fn.stat().st_size > 500:
        return u, dict(file=fn.name, ok=True, http="cached", ctype="")
    r = subprocess.run(["curl", "-sS", "-m", "90", "-L", "-H", f"User-Agent: {UA}", "-H", "Accept: image/*,*/*;q=0.8",
                        "-o", str(fn), "-w", "%{http_code} %{content_type}", u], capture_output=True, text=True)
    code, _, ctype = r.stdout.partition(" ")
    ok = code == "200" and ctype.startswith("image/") and fn.exists() and fn.stat().st_size > 500
    time.sleep(0.1)
    return u, dict(file=fn.name, ok=ok, http=code, ctype=ctype, err=r.stderr.strip()[:200])
todo = [u for u in sorted(urls) if not index.get(u, {}).get("ok")]
print("needed", len(urls), "todo", len(todo), flush=True)
with ThreadPoolExecutor(4) as ex:
    for n, (u, rec) in enumerate(ex.map(fetch, todo)):
        index[u] = rec
        if n % 100 == 0:
            json.dump(index, open(IDX, "w"), indent=1); print(n, flush=True)
json.dump(index, open(IDX, "w"), indent=1)
bad = [u for u in urls if not index[u]["ok"]]
print("done; failed", len(bad))
for u in bad: print(" ", index[u].get("http"), index[u].get("ctype"), u)
