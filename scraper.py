import asyncio
import aiohttp
from datetime import datetime

SOURCES = [
    "https://tw.xmm1993.top/sub?token=aniu",
    "https://all.xmm1993.top/sub?token=aniu",
    "https://h.xmm1993.top/sub?token=aniu",
    "https://jiedianfanqiang11111111.pages.dev/sub?token=a59061a1d9ac93e25cbbd3df4edec02a"
]

# 过滤阈值：低于200字符判定为无效内容
MIN_CONTENT_LEN = 200

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
            text = text.strip()
            print(f"[FETCH SUCCESS] {url} | Status: {r.status} | Length: {len(text)}")
            return text
    except Exception as e:
        print(f"[FETCH FAILED] {url} | Error: {str(e)[:80]}")
        return ""

def deduplicate_sub(raw_lines):
    """简易去重：剔除重复订阅行"""
    seen = set()
    unique = []
    for line in raw_lines:
        line = line.strip()
        if line and line not in seen:
            seen.add(line)
            unique.append(line)
    return unique

async def main():
    print("===== Scraper Start =====")
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    all_raw_content = []

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*(fetch(session, u) for u in SOURCES))

    # 筛选有效内容
    valid_content = []
    for idx, content in enumerate(results):
        if len(content) >= MIN_CONTENT_LEN:
            valid_content.append(content)
            all_raw_content.extend(content.splitlines())

    # 全局去重
    dedup_lines = deduplicate_sub(all_raw_content)

    # 写入规整文件
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(f"更新时间: {now_time}\n")
        f.write(f"有效源数量: {len(valid_content)}\n")
        f.write(f"去重后节点总数: {len(dedup_lines)}\n")
        f.write("=" * 50 + "\n\n")
        f.write("\n".join(dedup_lines))

    print(f"\n===== Scraper Done =====")
    print(f"有效源：{len(valid_content)} 个")
    print(f"去重后剩余独立节点：{len(dedup_lines)} 条")

if __name__ == "__main__":
    asyncio.run(main())
