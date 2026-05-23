import asyncio
import aiohttp
from datetime import datetime

SOURCES = [
    "https://tw.xmm1993.top/sub?token=aniu",
    "https://all.xmm1993.top/sub?token=aniu",
    "https://h.xmm1993.top/sub?token=aniu",
    "https://jiedianfanqiang11111111.pages.dev/sub?token=a59061a1d9ac93e25cbbd3df4edec02a"
]

async def fetch(session, url):
    try:
        async with session.get(
            url,
            timeout=aiohttp.ClientTimeout(total=20),
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
        ) as r:
            text = await r.text()
            print(f"[FETCH SUCCESS] {url} | Status: {r.status} | Length: {len(text)}")
            return text.strip()
    except Exception as e:
        print(f"[FETCH FAILED] {url} | Error: {str(e)[:80]}")
        return ""

async def main():
    print("===== Scraper Start =====")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    valid_content = []

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*(fetch(session, u) for u in SOURCES))

    # 筛选有效内容
    for idx, content in enumerate(results):
        if content:
            valid_content.append(f"\n# Source {idx+1} | Time: {now_time}\n{content}")

    # 写入本地文件
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(f"Update Time: {now_time}\nValid Source Count: {len(valid_content)}\n")
        f.writelines(valid_content)

    print(f"\n===== Scraper Done =====")
    print(f"Valid sources total: {len(valid_content)}")

if __name__ == "__main__":
    asyncio.run(main())
