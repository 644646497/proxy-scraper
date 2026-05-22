import asyncio
import aiohttp
import re
import time

# ===== 配置 =====
TIMEOUT = 10
CONCURRENCY = 20

TEST_URL = "https://www.google.com/generate_204"

# 延迟阈值（ms）
MAX_LATENCY = 800

patterns = [
    r'ss://[^\s"\']+',
    r'ssr://[^\s"\']+',
    r'vmess://[^\s"\']+',
    r'trojan://[^\s"\']+',
    r'vless://[^\s"\']+',
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ===== 读取 sources =====
with open("sources.txt", "r") as f:
    sources = [i.strip() for i in f if i.strip()]

nodes = set()
sem = asyncio.Semaphore(CONCURRENCY)

# ===== 抓取网页 =====
async def fetch(session, url):
    async with sem:
        try:
            async with session.get(url, timeout=TIMEOUT, headers=headers) as resp:
                return await resp.text()
        except:
            return ""

# ===== 测速函数 =====
async def test_node(session, node):
    try:
        start = time.time()

        async with session.get(TEST_URL, proxy=node, timeout=TIMEOUT) as resp:
            if resp.status != 204:
                return None

        latency = (time.time() - start) * 1000

        if latency > MAX_LATENCY:
            return None

        return (node, latency)

    except:
        return None

# ===== 主流程 =====
async def main():
    async with aiohttp.ClientSession() as session:

        # 1. 抓源
        tasks = [fetch(session, url) for url in sources]
        pages = await asyncio.gather(*tasks)

        for text in pages:
            for p in patterns:
                for n in re.findall(p, text):
                    nodes.add(n.strip())

        print(f"[+] raw nodes: {len(nodes)}")

        # 2. 测速
        print("[+] testing nodes...")

        results = await asyncio.gather(
            *[test_node(session, n) for n in list(nodes)]
        )

        valid = [r for r in results if r]

        print(f"[+] valid nodes: {len(valid)}")

        # 3. 排序（按延迟）
        valid.sort(key=lambda x: x[1])

        # 4. 输出
        with open("sub.txt", "w", encoding="utf-8") as f:
            for node, lat in valid:
                f.write(f"{node}\n")

        print("[+] saved sub.txt")

asyncio.run(main())
