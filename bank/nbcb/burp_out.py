#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from mitmproxy import http
import re
from hacknbcb import HackNBCB


def request(flow: http.HTTPFlow) -> None:
    netloc = flow.request.headers["Host"]
    body = flow.request.content
    if "X-GW-DATA-ENCRYPT-VERSION" in flow.request.headers and "nbcb.com.cn" in netloc:
        _, flow.request.content = HackNBCB().request_encrypt_by_common(b"", body)
        print(flow.request.content)
    elif flow.request.host == "iib-wechat.nbcb.com.cn":
        _, new_body = HackNBCB().request_encrypt_by_comma(b"", body)


# --no-http2
# --no-ssl-insecure

def response(flow: http.HTTPFlow) -> None:
    # 将响应头中新增了一个自定义头字段
    uri = flow.request.url
    netloc = flow.request.headers["Host"]
    if "encrypt.js" in uri and "nbcb.com.cn" in netloc:
        body = flow.response.content
        regex = re.compile(r"return \S+?uuid\(16,16\)")
        new_body = re.sub(regex, 'return "F8D08904F8B8BE2D"', body.decode())
        flow.response.content = new_body.encode()
    elif "X-GW-DATA-ENCRYPT-VERSION" in flow.request.headers and "nbcb.com.cn" in netloc:
        body = flow.response.content
        print(body)
        _, flow.response.content = HackNBCB().response_decrypt_by_common(b"", body)
