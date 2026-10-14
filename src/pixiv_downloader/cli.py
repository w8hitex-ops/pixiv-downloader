"""Pixiv 下载器入口。

用法：
    python main.py author   <author_id>
    python main.py bookmark <user_id>
    python main.py illust   <illust_id>
"""
import argparse
import os
import sys

from config import HEADERS, PROXIES          # ← 保持，config 在项目根
from .client import PixivClient              # ← 改成相对导入
from .api import PixivAPI
from .downloader import Downloader

# from config import HEADERS, PROXIES
# from pixiv_client import PixivClient
# from pixiv_api import PixivAPI
# from pixiv_downloader import Downloader

OUTPUT_DIR = "./output"


def cmd_author(api: PixivAPI, dl: Downloader, author_id: str) -> None:
    save_dir = os.path.join(OUTPUT_DIR, "ByUsers", author_id)
    for illust_id in api.get_illusts_by_author(author_id):
        urls = api.get_illust_urls(illust_id)
        if urls:
            dl.download_illust(illust_id, urls, save_dir)


def cmd_bookmark(api: PixivAPI, dl: Downloader, user_id: str) -> None:
    save_dir = os.path.join(OUTPUT_DIR, "ByBookmarks", user_id)
    for illust_id in api.get_illusts_by_bookmark(user_id):
        urls = api.get_illust_urls(illust_id)
        if urls:
            dl.download_illust(illust_id, urls, save_dir)


def cmd_illust(api: PixivAPI, dl: Downloader, illust_id: str) -> None:
    urls = api.get_illust_urls(illust_id)
    if not urls:
        print(f"未获取到作品 {illust_id} 的图片")
        return
    save_dir = os.path.join(OUTPUT_DIR, "ByIllust", illust_id)
    dl.download_illust(illust_id, urls, save_dir)


def main() -> int:
    parser = argparse.ArgumentParser(description="Pixiv 图片下载器")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_author = sub.add_parser("author", help="按作者 ID 下载全部作品")
    p_author.add_argument("author_id")

    p_bookmark = sub.add_parser("bookmark", help="按用户 ID 下载收藏夹")
    p_bookmark.add_argument("user_id")

    p_illust = sub.add_parser("illust", help="按作品 ID 下载单个作品")
    p_illust.add_argument("illust_id")

    args = parser.parse_args()

    client = PixivClient(HEADERS, PROXIES)
    api = PixivAPI(client)
    dl = Downloader(client)

    if args.mode == "author":
        cmd_author(api, dl, args.author_id)
    elif args.mode == "bookmark":
        cmd_bookmark(api, dl, args.user_id)
    elif args.mode == "illust":
        cmd_illust(api, dl, args.illust_id)

    return 0


if __name__ == "__main__":
    sys.exit(main())