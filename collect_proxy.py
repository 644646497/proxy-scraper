import requests

# 把公开订阅链接填到这里
urls = [
    "https://raw.githubusercontent.com/free-nodes/clashfree/refs/heads/main/clash20260512.yml",
    # 可以继续加更多链接，每行一个，用逗号隔开
]

all_proxies = set()

for url in urls:
    try:
        resp = requests.get(url, timeout=30)
        for line in resp.text.splitlines():
            line = line.strip()
            if line and not line.startswith('#'):
                all_proxies.add(line)
        print(f"从 {url} 获取 {len(resp.text.splitlines())} 行")
    except Exception as e:
        print(f"失败: {url} - {e}")

with open('proxies.txt', 'w') as f:
    for proxy in all_proxies:
        f.write(proxy + '\n')

print(f"共 {len(all_proxies)} 个节点")
