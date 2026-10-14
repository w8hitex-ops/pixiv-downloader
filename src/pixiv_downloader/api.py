"""三种模式的 Pixiv API 封装：按作者、按收藏夹、按作品。"""
import json
from typing import Iterator

from .client import PixivClient
# from pixiv_client import PixivClient


class PixivAPI:
    def __init__(self, client: PixivClient):
        self.client = client

    # ---------- 模式 1：按作者 ID 获取作品列表 ----------
    def get_illusts_by_author(self, author_id: str) -> Iterator[str]:
        """获取作者的全部作品 ID。"""
        url = (
            f"https://www.pixiv.net/ajax/user/{author_id}/profile/all"
            f"?sensitiveFilterMode=userSetting&lang=zh"
        )
        data = self.client.get_json(url)
        illusts = data["body"]["illusts"]
        for illust_id in illusts:
            yield illust_id

    # ---------- 模式 2：按用户 ID 获取收藏夹 ----------
    def get_illusts_by_bookmark(self, user_id: str, limit: int = 100) -> Iterator[str]:
        """分页获取某用户收藏夹里的所有作品 ID。"""
        offset = 0
        while True:
            url = (
                f"https://www.pixiv.net/ajax/user/{user_id}/illusts/bookmarks"
                f"?tag=&offset={offset}&limit={limit}&rest=show&lang=zh"
            )
            data = self.client.get_json(url)
            works = data["body"]["works"]
            if not works:
                break
            for w in works:
                yield w["id"]
            offset += limit

    # ---------- 模式 3：按作品 ID 获取所有分页 URL ----------
    def get_illust_urls(self, illust_id: str) -> list[str]:
        """获取单个作品的所有原图 URL。"""
        url = f"https://www.pixiv.net/ajax/illust/{illust_id}/pages?lang=zh"
        try:
            data = self.client.get_json(url)
        except RuntimeError as e:
            print(f"获取作品 {illust_id} 失败：{e}")
            return []

        pages = data.get("body", [])
        return [p["urls"]["original"] for p in pages]