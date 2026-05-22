import asyncio
import aiohttp
import re
import time

# ===== 配置 =====
TIMEOUT = 15
CONCURRENCY = 10
DELAY = 1  # 防止TG限流

patterns = [
    r'ss://[^\s"\'<]+',
    r'ssr://[^\s"\'<]+',
    r'vmess://[^\s"\'<]+',
    r'trojan://[^\s"\'<]+',
    r'vless://[^\s"\'<]+',
    r'hy2://[^\s"\'<]+'
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

# ===== 读取源 =====
with open("sources.txt", "r") as f:
    sources = [i.strip() for i in f.readlines() if i.strip()]

# ===== 存储结果 =====
nodes = set()
sem = asyncio.Semaphore(CONCURRENCY)

async def fetch(session, url):
    async with sem:
        try:
            async with session.get(url, timeout=TIMEOUT, headers=headers) as resp:
                text = await resp.text()
                return url, text
        except Exception as e:
            print(f"[-] Error: {url} -> {e}")
            return url, ""

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in sources]

        results = await asyncio.gather(*tasks)

        for url, text in results:
            print(f"[+] parsed: {url}")

            for p in patterns:
                for node in re.findall(p, text):
                    nodes.add(node.strip())

            time.sleep(DELAY)

    # ===== 输出 =====
    print(f"Total nodes: {len(nodes)}")

    with open("sub.txt", "w", encoding="utf-8") as f:
        for n in nodes:
            f.write(n + "\n")

    print("Saved sub.txt")

asyncio.run(main())
