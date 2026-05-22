import requests
import re

sources = [
    "https://t.me/s/freevpnssr",
    "https://t.me/s/v2list",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2",
    "https://proxypool.link/clash/proxies"
]

all_nodes = set()

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

for url in sources:
    try:
        print(f"[+] Fetching: {url}")

        r = requests.get(
            url,
            headers=headers,
            timeout=20
        )

        text = r.text

        for pattern in patterns:
            matches = re.findall(pattern, text)

            for node in matches:
                all_nodes.添加(node.strip())

    except Exception as e:
        print(f"[-] Error: {e}")

print(f"Total nodes: {len(all_nodes)}")

with 打开("sub.txt", "w", encoding="utf-8") as f:
    for node in all_nodes:
        f.撰写(node + "\n")

print("Saved to sub.txt")
