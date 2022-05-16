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
    new_urls = []
    for url in urls:
        try:
            url = unquote_plus(url.strip())
            res = urlparse(
                url, allow_fragments=True, scheme='http'
            )
        except:
            continue
        print(url)
        scheme = res[0]
        netloc = res[1]
        # add default path "/"
        path = res[2] if res[2] else '/'
        paths = path.split("/")
        # paths.remove("")
        # del extension judge exist "."
        if "." in paths[-1]:
            paths = paths[:-1]
        paths = [p for p in paths if p]
        # print(paths)
        # add default domain
        # e.g https://www.baidu.com/
        new_urls.append(urlunparse((scheme, netloc, '/', '', '', '')))
        for l in range(level):
            new_path = [""] + paths[:level] + [""]
            new_urls.append(urlunparse((scheme, netloc, "/".join(new_path), '', '', '')))
    return new_urls


def url_split_level_from_file(url_file, level):
    with open(url_file, 'r', encoding='UTF-8') as f:
        urls = f.readlines()
    level_urls = url_split_level(urls, level)
    level_urls = sorted(list(set(level_urls)), key=level_urls.index)
    return level_urls


def url_split_level_file_to_file(from_file, to_file, level):
    level_urls = url_split_level_from_file(from_file, level)
    with open(to_file, 'w', encoding='UTF-8') as f:
        level_urls = [url + '\n' for url in level_urls]
        f.writelines(level_urls)


if __name__ == "__main__":
    level = 2
    from_file = "./urls.txt"
    to_file = "./urls-level-{}.txt".format(level)
    url_split_level_file_to_file(from_file, to_file, level)
