import asyncio
import aiohttp
import requests
import base64

# 源节点地址
RAW_SOURCE = "https://raw.githubusercontent.com/644646497/proxy-scraper/refs/heads/main/output.txt"
TEST_TARGET = "https://www.baidu.com"
TIMEOUT = 5
CONCUR_TASK = 60

# 输出文件
RAW_OK = "valid_nodes.txt"
CLASH_SUB = "clash_sub.txt"
B64_SUB = "base64_sub.txt"

def get_proxy_list():
    res = requests.get(RAW_SOURCE, timeout=15)
    res.raise_for_status()
    lines = [i.strip() for i in res.text.splitlines() if i.strip()]
    print(f"读取原始节点：{len(lines)} 个")
    return lines

async def check_one(session, proxy):
    try:
        async with session.get(
            TEST_TARGET,
            proxy=f"http://{proxy}",
            timeout=aiohttp.ClientTimeout(total=TIMEOUT)
        ) as resp:
            return resp.status == 200
    except:
        return False

async def batch_check(proxy_list):
    conn = aiohttp.TCPConnector(limit=CONCUR_TASK)
    async with aiohttp.ClientSession(connector=conn) as sess:
        tasks = [check_one(sess, p) for p in proxy_list]
        results = await asyncio.gather(*tasks)
    ok = [proxy for proxy, flag in zip(proxy_list, results) if flag]
    return ok

# 组装Clash标准订阅格式
def build_clash_sub(nodes):
    clash_lines = []
    for item in nodes:
        ip, port = item.split(":")
        clash_lines.append(f"- {ip}:{port}")
    return "\n".join(clash_lines)

def main():
    origin_proxies = get_proxy_list()
    usable = asyncio.run(batch_check(origin_proxies))
    print(f"测速可用节点：{len(usable)} 个")

    # 1. 纯节点文本
    with open(RAW_OK, "w", encoding="utf-8") as f:
        f.write("\n".join(usable))

    # 2. Clash订阅明文
    clash_content = build_clash_sub(usable)
    with open(CLASH_SUB, "w", encoding="utf-8") as f:
        f.write(clash_content)

    # 3. Base64编码通用订阅
    b64_data = base64.b64encode(clash_content.encode("utf-8")).decode("utf-8")
    with open(B64_SUB, "w", encoding="utf-8") as f:
        f.write(b64_data)

    print("订阅文件生成完毕")
    print("==== 使用说明 ====")
    print("Clash客户端：导入 clash_sub.txt 内容")
    print("通用订阅链接类客户端：使用 base64_sub.txt 内编码字符串")

if __name__ == "__main__":
    main()
