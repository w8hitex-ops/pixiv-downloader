"""统一的 Pixiv 请求客户端：集中处理重试、限流、代理、SSL。"""
import random
import time
import json

import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 关闭 verify=False 带来的警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class PixivClient:
    """封装 requests.Session，统一处理代理、重试、限流。"""

    def __init__(self, headers: dict, proxies: dict | None = None):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.proxies = proxies

        # 遇到 429 / 5xx 自动重试，指数退避
        retry = Retry(
            total=5,
            backoff_factor=2,  # 2s, 4s, 8s, 16s...
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

    def get(self, url: str, *, sleep: bool = True, **kwargs) -> requests.Response:
        """发 GET 请求，默认加随机延迟，避免触发限流。"""
        if sleep:
            time.sleep(random.uniform(0.5, 2.0))
        kwargs.setdefault("timeout", 20)
        kwargs.setdefault("verify", False)
        return self.session.get(url, proxies=self.proxies, **kwargs)

    def get_json(self, url: str, **kwargs) -> dict:
        """GET 并解析 JSON，任何异常都抛出来，方便上层处理。"""
        resp = self.get(url, **kwargs)
        if resp.status_code != 200:
            raise RuntimeError(f"HTTP {resp.status_code}: {url}")
        try:
            return json.loads(resp.text)
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"返回非 JSON (可能是 429/403)：{resp.text[:200]}"
            ) from e