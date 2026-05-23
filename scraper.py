import aiohttp
import asyncio
import base64
import re
from urllib.parse import urlparse

# =====================
# SOURCES（你已升级版）
# =====================
SOURCES = [
    "https://raw.githubusercontent.com/sangosbanikz/proxy-pool/main/n3.txt",
    "https://raw.githubusercontent.com/sangosbanikz/proxy-pool/main/n2.txt",
    "https://tw.xmm1993.top/sub?token=aniu",
    "https://all.xmm1993.top/sub?token=aniu",
    "https://h.xmm1993.top/sub?token=aniu",
    "https://jiedianfanqiang11111111.pages.dev/sub?token=a59061a1d9ac93e25cbbd3df4edec02a"
]

# =====================
# REGEX
# =====================
PATTERNS = [
    r"ss://[^\s]+",
    r"vmess://[^\s]+",
    r"trojan://[^\s]+",
    r"vless://[^\s]+"
]

# =====================
# SOURCE SCORE
# =====================
source_score = {}

# =====================
# FETCH
# =====================
async def fetch(session, url):
    try:
        async with session.get(url, timeout=15) as r:
            text = await r.text()
            return url, text
    except:
        return url, ""

# =====================
# PARSE
# =====================
def parse(text):
    nodes = set()

    # base64 fallback
    if text.strip().startswith("c3M") or "://" not in text:
        try:
            text = base64.b64decode(text + "==").decode()
        except:
            pass

    for p in PATTERNS:
        nodes.update(re.findall(p, text))

    return nodes

# =====================
# SIMPLE NODE KEY
# =====================
def node_key(node):
    try:
        u = urlparse(node)
        return f"{u.hostname}:{u.port}:{u.username}"
    except:
        return node

# =====================
# TEST NODE (lightweight)
# =====================
async def test_node(node):
    try:
        u = urlparse(node)
        host = u.hostname
        port = u.port or 443

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=3
        )
        writer.close()
        await writer.wait_closed()
        return node
    except:
        return None

# =====================
# GROUP
# =====================
def group(node):
    u = urlparse(node)
    host = (u.hostname or "").upper()

    if any(x in host for x in ["US", "USA"]):
        return "US"
    if "HK" in host:
        return "HK"
    if "JP" in host:
        return "JP"
    if any(x in host for x in ["SG", "SING"]):
        return "SG"
    if any(x in host for x in ["DE", "FR", "NL", "UK"]):
        return "EU"
    return "OTHER"

# =====================
# MAIN
# =====================
async def main():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*(fetch(session, u) for u in SOURCES))

    all_nodes = set()
    valid_sources = 0

    for url, text in results:
        nodes = parse(text)

        if len(nodes) == 0:
            source_score[url] = source_score.get(url, 0) - 3
            continue

        valid_sources += 1
        source_score[url] = source_score.get(url, 0) + 2

        all_nodes.update(nodes)

    print("[+] raw nodes:", len(all_nodes))

    # 去重
    dedup = {}
    for n in all_nodes:
        dedup[node_key(n)] = n

    nodes = list(dedup.values())

    # 测速
    tasks = [test_node(n) for n in nodes]
    results = await asyncio.gather(*tasks)

    valid = [x for x in results if x]

    print("[+] valid nodes:", len(valid))

    # 分组
    grouped = {}
    for n in valid:
        g = group(n)
        grouped.setdefault(g, []).append(n)

    # 输出
    with open("valid_nodes.txt", "w", encoding="utf-8") as f:
        for g, ns in grouped.items():
            f.write(f"\n# {g}\n")
            for n in ns:
                f.write(n + "\n")

    print("[+] done")

if __name__ == "__main__":
    asyncio.run(main())
