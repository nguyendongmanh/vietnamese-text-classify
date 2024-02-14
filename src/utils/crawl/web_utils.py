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
        raise HTTPError("There are some mistakes when making a request to url")
    soup = BeautifulSoup(response.text, "lxml")
    return soup


def join_with_root(path: str = None):
    return urljoin(ROOT_URL, path)


def is_path(path: str = None):
    return "http" not in path


def is_valid_url(path: str = None):
    return not (("collection" in path) or (len(path.split("/")) == 2))
