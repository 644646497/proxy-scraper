import requests
import re
import base64

keywords = ['ss://', 'vmess://', 'trojan://', 'ssr://']
query = ' '.join(keywords)
url = f'https://api.github.com/search/code?q={query}&per_page=30'
headers = {'Accept': 'application/vnd.github.v3+json'}

def extract_proxies(text):
    patterns = [
        r'ss://[A-Za-z0-9]+@[A-Za-z0-9.-]+:\d+',
        r'vmess://[A-Za-z0-9+/=]+',
        r'trojan://[A-Za-z0-9]+@[A-Za-z0-9.-]+:\d+',
        r'ssr://[A-Za-z0-9+/=]+',
    ]
    proxies = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        proxies.extend(matches)
    return proxies

all_proxies = set()

try:
    resp = requests.get(url, headers=headers)
    data = resp.json()
    for item in data.get('items', []):
        file_url = item['url']
        try:
            file_resp = requests.get(file_url, headers=headers)
            content = file_resp.json().get('content', '')
            if content:
                decoded = base64.b64decode(content).decode('utf-8', errors='ignore')
                proxies = extract_proxies(decoded)
                all_proxies.update(proxies)
        except:
            pass
    
    with open('proxies.txt', 'w') as f:
        for proxy in all_proxies:
            f.write(proxy + '\n')
    print(f"找到 {len(all_proxies)} 个节点")
except Exception as e:
    print(f"错误: {e}")
