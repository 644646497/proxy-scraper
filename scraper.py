import asyncio
import aiohttp

SOURCES = [
    "https://example.com/data1.txt",
    "https://example.com/data2.txt"
]

async def fetch(session, url):
    try:
        async with session.get(url, timeout=20) as r:
            text = await r.text()
            print("[FETCH]", url, r.status, len(text))
            return url, text
    except Exception as e:
        print("[ERROR]", url, e)
        return url, ""

def parse(text):
    """
    通用解析：按行提取非空数据
    适用于：URL / JSON line / text feed
    """
    items = set()
    for line in text.splitlines():
        line = line.strip()
        if line:
            items.add(line)
    return items

async def main():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(*(fetch(session, u) for u in SOURCES))

    all_items = set()

    for url, text in results:
        items = parse(text)

        print("[PARSE]", url, len(items))

        all_items.update(items)

    print("[TOTAL]", len(all_items))

    with open("output.txt", "w") as f:
        for i in sorted(all_items):
            f.write(i + "\n")

if __name__ == "__main__":
    asyncio.run(main())
