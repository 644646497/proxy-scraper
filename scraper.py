import asyncio
import aiohttp
import re
import time
import json

# ================= CONFIG =================
TIMEOUT = 10
CONCURRENCY = 20
MAX_LATENCY = 800

TEST_URL = "https://www.google.com/generate_204"

patterns = [
    r'ss://[^\s"\']+',
    r'ssr://[^\s"\']+',
    r'vmess://[^\s"\']+',
    r'trojan://[^\s"\']+',
    r'vless://[^\s"\']+'
]

# ================= LOAD SOURCES =================
with open("sources.txt", "r") as f:
    sources = [x.strip() for x in f if x.strip()]

nodes = set()
sem = asyncio.Semaphore(CONCURRENCY)

# ================= FETCH =================
async def fetch(session, url):
    async with sem:
        try:
            async with session.get(url, timeout=TIMEOUT) as r:
                return await r.text()
        except:
            return ""

# ================= TCP CHECK =================
async def tcp_check(session, proxy):
    try:
        start = time.time()
        async with session.get(TEST_URL, proxy=proxy, timeout=TIMEOUT) as r:
            if r.status != 204:
                return None
        return (time.time() - start) * 1000
    except:
        return None

# ================= SCORE =================
def score(latency):
    if latency is None:
        return 0
    if latency > 800:
        return 10
    return max(0, 100 - int(latency / 10))

# ================= CLASSIFY =================
def classify(n):
    n = n.lower()
    if "hk" in n or "hong" in n or "🇭🇰" in n:
        return "HK"
    if "us" in n or "usa" in n or "🇺🇸" in n:
        return "US"
    if "jp" in n or "japan" in n or "🇯🇵" in n:
        return "JP"
    return "OTHER"

# ================= MAIN =================
async def main():
    async with aiohttp.ClientSession() as session:

        # ---- fetch sources ----
        pages = await asyncio.gather(*[fetch(session, u) for u in sources])

        # ---- extract nodes ----
        for text in pages:
            for p in patterns:
                for n in re.findall(p, text):
                    nodes.add(n.strip())

        print("[+] raw nodes:", len(nodes))

        # ---- test nodes ----
        results = []

        async def worker(n):
            latency = await tcp_check(session, n)
            if latency is None:
                return None
            if latency > MAX_LATENCY:
                return None
            return {
                "node": n,
                "latency": latency,
                "score": score(latency),
                "group": classify(n)
            }

        results = await asyncio.gather(*[worker(n) for n in list(nodes)])
        valid = [r for r in results if r]

        print("[+] valid nodes:", len(valid))

        # ---- sort by score ----
        valid.sort(key=lambda x: x["score"], reverse=True)

        # ---- group ----
        groups = {"HK": [], "US": [], "JP": [], "OTHER": []}
        for v in valid:
            groups[v["group"]].append(v)

        # ---- output sub.txt ----
        with open("sub.txt", "w") as f:
            for v in valid:
                f.write(v["node"] + "\n")

        # ---- output grouped ----
        for k in groups:
            with open(f"{k}.txt", "w") as f:
                for v in groups[k]:
                    f.write(v["node"] + "\n")

        # ---- clash ----
        clash = {
            "proxies": [{"name": f"node-{i}", "url": v["node"]} for i, v in enumerate(valid)],
            "proxy-groups": [{
                "name": "AUTO",
                "type": "select",
                "proxies": [f"node-{i}" for i in range(len(valid))]
            }]
        }

        with open("clash.json", "w") as f:
            json.dump(clash, f, indent=2)

        # ---- sing-box ----
        singbox = {
            "outbounds": [
                {
                    "type": "selector",
                    "tag": "auto",
                    "outbounds": [v["node"] for v in valid]
                }
            ]
        }

        with open("singbox.json", "w") as f:
            json.dump(singbox, f, indent=2)

        print("[+] done")

asyncio.run(main())
