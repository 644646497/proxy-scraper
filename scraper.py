import asyncio
import aiohttp

SOURCES = [
    "https://example.com"
]

async def fetch(session, url):
    try:
        async with session.get(url) as r:
            text = await r.text()
            print("[FETCH]", url, r.status, len(text))
            return text
    except Exception as e:
        print("[ERROR]", e)
        return ""

async def main():
    print("START")

    async with aiohttp.ClientSession() as session:
        for url in SOURCES:
            await fetch(session, url)

    print("DONE")

if __name__ == "__main__":
    asyncio.run(main())
