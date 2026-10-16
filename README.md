![python](https://img.shields.io/badge/python-3.8%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![stars](https://img.shields.io/github/stars/w8hitex-ops/pixiv-downloader)


# Pixiv Downloader

一个简洁的 Pixiv 图片下载工具，支持三种下载模式。

## ✨ 功能特性

- [x] 按作者 ID 下载该作者的全部作品
- [x] 按用户 ID 下载该用户的收藏夹
- [x] 按作品 ID 下载单个作品的所有分页
- [x] 支持代理（HTTP/HTTPS）
- [x] 自动重试、随机延迟
- [ ] 动图下载（开发中）


## 📦 安装

```bash
git clone https://github.com/w8hitex-ops/pixiv-downloader.git
cd pixiv-downloader
pip install -r requirements.txt
```

## ⚙️ 配置

复制配置模板并填入你的信息：

```bash
cp config.example.py config.py
```

编辑 `config.py`：

```python
HEADERS = {
    "User-Agent": "Mozilla/5.0 ...",
    "referer": "https://www.pixiv.net/",
    "Cookie": "你的 Cookie（从浏览器复制）"
}

PROXIES = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}
```

> 💡 如何获取 Cookie：登录 Pixiv 后，按 F12 打开开发者工具 → Network → 刷新页面 → 复制任意请求的 Cookie。

> ⚠️ `config.py` 已被 `.gitignore` 忽略，不会上传到 GitHub，请放心填写。

## 🚀 使用

### 按作者 ID (123456)下载

```bash
python main.py author 123456
```

### 按用户收藏夹 ID (123456)下载

```bash
python main.py bookmark 123456
```

### 按作品 ID (123456)下载

```bash
python main.py illust 123456
```

下载的图片会保存在 `./output/` 目录下，按作者 ID 分文件夹。

## 📁 项目结构

```
pixiv-downloader/
├── main.py              # 命令行入口
├── config.example.py    # 配置模板
├── scr/
    ├──pixiv_downloader/
        ├── cli.py
        ├── client.py        # 请求封装（重试、限流、代理）
        ├── api.py       # API 解析（三种模式）
        └── downloader.py    # 下载核心
└── requirements.txt
```

## 🛠️ 常见问题

**Q: 遇到 429 Too Many Requests 怎么办？**

A: 项目已内置随机延迟和自动重试。如果仍频繁出现，请降低请求频率或更换代理节点。

**Q: 遇到 `check_hostname requires server_hostname`？**

A: 这是代理配置问题。请确保 `PROXIES` 中 `https` 的值是 `http://` 开头，而不是 `https://`。

**Q: Cookie 过期了怎么办？**

A: 重新从浏览器复制新的 Cookie，更新 `config.py` 即可。

## 📝 TODO

- [ ] 支持多线程下载
- [ ] 支持按标签筛选
- [ ] 图形界面

## 📄 License

MIT License

## ⚠️ 免责声明

本项目仅供学习交流使用，请勿用于商业用途。下载的图片版权归原作者所有。
