# config.example.py
# 复制这个文件为 config.py，然后填入你自己的 Cookie

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    "referer": "https://www.pixiv.net/",
    # 从浏览器 F12 -> Network 复制完整的 Cookie 字符串
    "Cookie": "把你的 Cookie 粘贴到这里",
}

PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}