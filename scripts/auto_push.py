import requests
import re
import json
from datetime import datetime

target_urls = [
    "https://github.com/MatinGhanbari/v2ray-configs",
    "https://github.com/barry-far/V2ray-Config",
    "https://github.com/18519194800/-"
]

pattern = re.compile(r'https://raw\.githubusercontent\.com/[^\s"\'()]+?\.(txt|yaml)')
headers = {"User-Agent": "Mozilla/5.0"}
valid_links = []

for url in target_urls:
    try:
        html = requests.get(url, headers=headers, timeout=15).text
        for link in set(re.findall(pattern, html)):
            try:
                r = requests.head(link, timeout=10)
                if r.status_code == 200:
                    valid_links.append(link)
            except:
                continue
    except Exception as e:
        print(f"[!] 访问失败：{url}，错误：{e}")

with open("valid_links.txt", "w", encoding="utf-8") as f:
    f.write(f"# 更新时间：{datetime.now()}\n")
    for link in valid_links:
        f.write(link + "\n")  # ✅ 修复换行

substore_data = {
    "subs": [{"name": f"订阅{i+1}", "url": link} for i, link in enumerate(valid_links)]
}
with open("substore.json", "w", encoding="utf-8") as f:
    json.dump(substore_data, f, indent=2, ensure_ascii=False)

with open("substore_url.txt", "w", encoding="utf-8") as f:
    f.write("|".join(valid_links))

print(f"✅ 共获取到 {len(valid_links)} 条有效订阅链接")
