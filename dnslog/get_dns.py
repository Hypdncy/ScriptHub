# -*- coding: utf-8 -*-


import requests
from urllib.parse import urlparse
from common.net.utils import get_ips_by_mask


def get_hostname_real_ip(url, ips):
    hostname = urlparse(url).hostname
    for ip in ips:
        headers = {
            "Host": f"{hostname}",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        }
        new_url = url.replace(hostname, ip, 1)
        print(new_url)
        try:
            res = requests.get(url=new_url, headers=headers, verify=False, timeout=5)
            if res.status_code == 200 and "您的请求已提交，系统返回如下信息" not in res.text:
                print(hostname, ip, res.status_code)
        except:
            pass


if __name__ == "__main__":
    urls = [
        "https://ev.zt906.com/",
        "https://dap.zt906.com",
        # "https://115.238.88.202:1443/",
        "http://www.htuo56.com/",
        "http://saaswms.zt906.com/",
        "http://wms.zmd.com.cn:8999",
        # "http://120.132.241.224:53797/stamp/",
        # "http://120.132.241.224:53797/",
        "https://emms.zmd.com.cn/",
        "https://wms-uw.zmd.com.cn/",
        "https://m-portal.zmd.com.cn:18886",
        "https://m-portal.zmd.com.cn:18998",
        "https://m-portal.zmd.com.cn:18443",
    ]
    ip = "120.132.241.224"
    mask = 28
    ips = get_ips_by_mask(ip, 26)
    print(ips)
    for url in urls:
        get_hostname_real_ip(url, ips)
