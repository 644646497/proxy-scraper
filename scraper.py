def parse(text):
    nodes = set()

    if not text:
        return nodes

    # 强制提取所有协议
    import re

    patterns = [
        r"vless://[^\s]+",
        r"vmess://[^\s]+",
        r"trojan://[^\s]+",
        r"ss://[^\s]+"
    ]

    for p in patterns:
        nodes.update(re.findall(p, text))

    # fallback base64（更宽松）
    try:
        decoded = base64.b64decode(text + "==").decode(errors="ignore")
        for p in patterns:
            nodes.update(re.findall(p, decoded))
    except:
        pass

    return nodes
