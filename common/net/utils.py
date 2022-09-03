# -*- coding: utf-8 -*-

from urllib.parse import urlparse, urlunparse, unquote_plus

from IPy import IP


def get_ips_by_mask(ip, mask, is_public=False):
    l_ips = []
    try:
        ips = IP(ip).make_net(mask)
        for ip in ips:
            if (not is_public) or ip.iptype() == 'PUBLIC':
                l_ips.append(ip.strNormal())
    except Exception as e:
        print(ip, mask)
    return l_ips


def get_ips_from_file(filename, mask=30):
    l_ips = set([])
    with open(filename, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.strip():
            tmp_l_ips = get_ips_by_mask(line.strip(), mask)
            # l_ips.add(tmp_l_ips)
            l_ips.update(tmp_l_ips)
    l_ips = list(l_ips)
    l_ips.sort(key=lambda x: IP(x).ip)

    return l_ips


def get_ips_from_file_to_file(srcFile, dstFile, mask=30):
    l_ips = get_ips_from_file(srcFile, mask)
    with open(dstFile, 'w') as f:
        f.writelines([ip + '\n' for ip in l_ips])


def get_url_split_level(urls, level=0):
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


def get_url_split_level_from_file(url_file, level):
    with open(url_file, 'r', encoding='UTF-8') as f:
        urls = f.readlines()
    level_urls = get_url_split_level(urls, level)
    level_urls = sorted(level_urls)
    return level_urls


def get_url_split_level_file_to_file(from_file, to_file, level):
    level_urls = get_url_split_level_from_file(from_file, level)
    with open(to_file, 'w', encoding='UTF-8') as f:
        level_urls = [url + '\n' for url in level_urls]
        f.writelines(level_urls)


if __name__ == "__main__":
    mask = 29
    from_file = "ips.txt"
    to_file = "./ips-{}.txt".format(mask)
    get_ips_from_file_to_file(from_file, to_file, mask)

    level = 2
    from_file = "urls.txt"
    to_file = "./urls-level-{}.txt".format(level)
    get_url_split_level_file_to_file(from_file, to_file, level)
