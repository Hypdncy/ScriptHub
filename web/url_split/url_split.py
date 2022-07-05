from urllib.request import Request

import requests
import uuid
import time
import re
from urllib.parse import urlparse, urlunparse, quote_plus, quote, quote_from_bytes, unquote_plus, unquote
import logging
from http.cookies import SimpleCookie

# cookies = requests.utils.dict_from_cookiejar(req.cookies)  # 转成字典格式
from requests.cookies import get_cookie_header


def url_split_level(urls, level=0):
    new_urls = set([])
    for url in urls:
        try:
            url = unquote_plus(url.strip())
            res = urlparse(
                url, allow_fragments=True, scheme='http'
            )
            scheme = res.scheme
            netloc = res.netloc
            path = res.path if res.path else '/'
        except:
            continue
        paths = path.split("/")

        print(paths)
        if "." in paths[-1]:
            paths[-1] = ""

        paths = [p for p in paths if p]
        new_urls.add(urlunparse((scheme, netloc, '/', '', '', '')))
        for lev in range(1, level + 1):
            print(lev)
            new_path = [""] + paths[:lev] + [""]
            print("/".join(new_path))
            new_url = urlunparse((scheme, netloc, "/".join(new_path), '', '', ''))
            new_urls.add(new_url)
    new_urls = list(new_urls)
    return new_urls


def url_split_level_from_file(url_file, level):
    with open(url_file, 'r', encoding='UTF-8') as f:
        urls = f.readlines()
    level_urls = url_split_level(urls, level)
    level_urls = sorted(level_urls)
    return level_urls


def url_split_level_file_to_file(from_file, to_file, level):
    level_urls = url_split_level_from_file(from_file, level)
    with open(to_file, 'w', encoding='UTF-8') as f:
        level_urls = [url + '\n' for url in level_urls]
        f.writelines(level_urls)


if __name__ == "__main__":
    level = 2
    from_file = "urls.txt"
    to_file = "./urls-level-{}.txt".format(level)
    url_split_level_file_to_file(from_file, to_file, level)
