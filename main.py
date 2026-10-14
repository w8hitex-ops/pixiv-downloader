# main.py
"""Pixiv 下载器入口。

用法：
    python main.py author   <author_id>
    python main.py bookmark <user_id>
    python main.py illust   <illust_id>
"""
# main.py
"""项目入口，保持 python main.py ... 的用法不变。"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from pixiv_downloader.cli import main

if __name__ == "__main__":
    sys.exit(main())