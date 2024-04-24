import requests


def get_page(url: str) -> str:
    resp = requests.get(url)
    if resp.status_code != 200:
        raise RuntimeError(f"Can't get page for url={url}")
    return resp.text
