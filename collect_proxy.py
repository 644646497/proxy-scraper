import requests
import json
import base64

# 公开订阅源列表
urls = [
    "https://raw.githubusercontent.com/free-nodes/clashfree/refs/heads/main/clash20260512.yml",
]

all_proxies = []
node_lines = []

for url in urls:
    try:
        resp = requests.get(url, timeout=30)
        for line in resp.text.splitlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            # 检查是否是 Clash YAML 格式的节点
            if '{' in line and 'type: ss' in line:
                try:
                    # 解析 Clash 节点
                    part = line.split('{', 1)[1].rsplit('}', 1)[0]
                    import re
                    name = re.search(r'name:\s*([^,]+)', part)
                    server = re.search(r'server:\s*([^,]+)', part)
                    port = re.search(r'port:\s*(\d+)', part)
                    cipher = re.search(r'cipher:\s*([^,]+)', part)
                    password = re.search(r'password:\s*([^,]+)', part)
                    
                    if server and port and cipher and password:
                        # 转换成标准 ss:// 格式
                        auth = base64.b64encode(f"{cipher.group(1)}:{password.group(1)}".encode()).decode()
                        ss_link = f"ss://{auth}@{server.group(1)}:{port.group(1)}"
                        if name:
                            ss_link += f"#{name.group(1)}"
                        node_lines.append(ss_link)
                        all_proxies.append(ss_link)
                except:
                    pass
            # 检查是否已经是标准 ss:// 格式
            elif line.startswith('ss://') or line.startswith('vmess://') or line.startswith('trojan://'):
                node_lines.append(line)
                all_proxies.append(line)
        print(f"从 {url} 抓取 {len(node_lines)} 个节点")
    except Exception as e:
        print(f"失败: {url} - {e}")

# 生成订阅文件
with open('subscribe.txt', 'w') as f:
    for node in node_lines:
        f.write(node + '\n')

print(f"共 {len(all_proxies)} 个节点")
print("订阅文件: subscribe.txt")
