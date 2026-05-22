import requests
import json
import time

SOURCES = [
    "你的源1",
    "你的源2",
    "你的源3"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def fetch(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)

        # 🚨 关键1：过滤明显失败页面
        if r.status_code != 200:
            return None

        text = r.text.strip()

        # 🚨 关键2：过滤 Cloudflare / 空页面
        if "Just a moment" in text:
            return None
        if len(text) < 50:
            return None

        return text

    except:
        return None


def parse_nodes(text):
    """
    你原来的解析逻辑放这里
    """
    nodes = []

    # 示例：你自己替换解析规则
    for line in text.splitlines():
        if "://" in line:
            nodes.append(line.strip())

    return nodes


all_nodes = []

for url in SOURCES:
    print("[+] fetching:", url)

    data = fetch(url)

    if not data:
        print("[-] failed:", url)
        continue

    nodes = parse_nodes(data)

    print("[+] nodes:", len(nodes))

    all_nodes.extend(nodes)

    time.sleep(1)

# 去重
all_nodes = list(set(all_nodes))

print("\n[+] total nodes:", len(all_nodes))

# 输出
with open("nodes.txt", "w") as f:
    for n in all_nodes:
        f.write(n + "\n")

print("[+] done")
