"""图片下载：静态图 + 预留动图接口。"""
import os

# from pixiv_client import PixivClient
from .client import PixivClient

class Downloader:
    def __init__(self, client: PixivClient):
        self.client = client

    def download_illust(self, illust_id: str, urls: list[str], save_dir: str) -> None:
        """下载一个作品的所有分页。"""
        os.makedirs(save_dir, exist_ok=True)

        for idx, url in enumerate(urls):
            name = url.split("/")[-1]
            # 统一命名：{id}_p{idx}.{ext}
            ext = os.path.splitext(name)[-1] or ".jpg"
            filename = f"{illust_id}_p{idx}{ext}"
            path = os.path.join(save_dir, filename)

            if os.path.exists(path):
                print(f"已存在，跳过：{filename}")
                continue

            self._download_file(url, path)

    def _download_file(self, url: str, path: str) -> None:
        """下载单个文件，先写 .tmp，成功后原子替换，避免半截文件。"""
        try:
            resp = self.client.get(url)
            if resp.status_code != 200:
                print(f"下载失败 {resp.status_code}: {url}")
                return

            tmp = path + ".tmp"
            with open(tmp, "wb") as f:
                f.write(resp.content)
            os.replace(tmp, path)
            print(f"✓ {path}")

        except Exception as e:
            print(f"下载出错 {url}: {e}")

    def download_ugoira(self, illust_id: str, save_dir: str) -> None:
        """【预留】动图下载：未来先下 zip，再用 ffmpeg 合成。"""
        raise NotImplementedError("动图下载将在后续版本实现")