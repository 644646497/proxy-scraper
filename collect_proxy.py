import requests
import re
import base64

urls = [
    "https://raw.githubusercontent.com/free-nodes/clashfree/refs/heads/main/clash20260512.yml",
    "https://proxypool.link/ss/sub",
    "https://proxypool.link/sip002/sub",
    "https://proxypool.link/ssr/sub",
    "https://proxypool.link/vmess/sub",
    "https://proxypool.link/trojan/sub",
]

all_proxies = []

for url in urls:
    try:
        resp = requests.get(url, timeout=30)
        print(f"抓取: {url} - 状态码 {resp.status_code}")
        for line in resp.text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # 解析 Clash YAML 格式的节点
            if '{' in line and 'type: ss' in line:
                try:
                    part = line.split('{', 1)[1].rsplit('}', 1)[0]
                    name = re.search(r'name:\s*([^,]+)', part)
                    server = re.search(r'server:\s*([^,]+)', part)
                    port = re.search(r'port:\s*(\d+)', part)
                    cipher = re.search(r'cipher:\s*([^,]+)', part)
                    password = re.search(r'password:\s*([^,]+)', part)
                    
                    if server and port and cipher and password:
                        auth = base64.b64encode(f"{cipher.group(1)}:{password.group(1)}".encode()).decode()
                        ss_link = f"ss://{auth}@{server.group(1)}:{port.group(1)}"
                        if name:
                            ss_link += f"#{name.group(1)}"
                        all_proxies.append(ss_link)
                except:
                    pass
            elif line.startswith('ss://') or line.startswith('vmess://') or line.startswith('trojan://') or line.startswith('ssr://'):
                all_proxies.append(line)
        print(f"  当前已抓取 {len(all_proxies)} 个节点")
    except Exception as e:
        print(f"失败: {url} - {e}")

# 去重
all_proxies = list(dict.fromkeys(all_proxies))

with open('subscribe.txt', 'w') as f:
    for proxy in all_proxies:
        f.write(proxy + '\n')

print(f"共 {len(all_proxies)} 个节点（已去重）")
print("订阅地址: https://raw.githubusercontent.com/644646497/proxy-scraper/main/subscribe.txt")
