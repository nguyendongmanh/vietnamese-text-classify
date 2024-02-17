import requests
from config import Config
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from urllib.parse import urljoin

ROOT_URL = Config.ROOT_URL


def get_soup(url: str = None) -> BeautifulSoup:
    if url is None:
        raise HTTPError("ROOT URL is required ...")
    response = requests.get(url, headers=Config.HEADER, timeout=Config.TIMEOUT)
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, "lxml")
    pnf_title = soup.find("div", class_="pnf-title")
    if pnf_title:
        if "OOPS" in pnf_title.text:
            return None
    return soup


def join_with_root(path: str = None):
    return urljoin(ROOT_URL, path)


def is_path(path: str = None):
    return "http" not in path


def is_valid_url(path: str = None):
    return not (("collection" in path) or (len(path.split("/")) == 2))
