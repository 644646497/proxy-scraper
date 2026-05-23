import asyncio
import aiohttp

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
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        ) as r:

            text = await r.text()

            print("[FETCH]", url)
            print("[STATUS]", r.status)
            print("[LEN]", len(text))
            print(text[:120])

            return text

    except Exception as e:
        print("[ERROR]", url, e)
        return ""

async def main():
    print("START")

    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            *(fetch(session, u) for u in SOURCES)
        )

    total = 0

    for t in results:
        if t:
            total += 1

    print("[TOTAL SOURCES OK]", total)
    print("DONE")

if __name__ == "__main__":
    asyncio.run(main())
