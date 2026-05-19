cat > collect_proxy.py << 'EOF'
import requests

# 替换成你找到的公开订阅链接
urls = [
    # 示例格式，需要替换成真实地址
    # "https://raw.githubusercontent.com/用户名/仓库名/分支/文件名.txt",
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
EOF
