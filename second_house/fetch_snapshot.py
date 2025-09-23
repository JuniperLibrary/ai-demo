import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re

XIAOQU_URL = "https://m.ke.com/xa/xiaoqu/3820023227732700"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/115.0 Safari/537.36"
}

def fetch_snapshot(url):
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    html = r.text
    soup = BeautifulSoup(html, "html.parser")

    # 1) 尝试 CSS 选择器
    price_node = soup.select_one(".price .num")

    # 2) 如果没找到，用正则匹配整个 HTML
    avg_price = None
    if price_node:
        try:
            avg_price = float(price_node.get_text(strip=True).replace(",", ""))
        except ValueError:
            avg_price = None
    else:
        m = re.search(r"参考均价[：: ]*([\d,]+\.?\d*)\s*元/㎡", html)
        if m:
            avg_price = float(m.group(1).replace(",", ""))

    # 在售套数
    sale_count = None
    m2 = re.search(r"在售二手房[：: ]*([0-9]+)\s*套", html)
    if m2:
        sale_count = int(m2.group(1))

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "avg_price": avg_price,
        "sale_count": sale_count,
        "url": url
    }

if __name__ == "__main__":
    snap = fetch_snapshot(XIAOQU_URL)
    print("snapshot:", snap)
