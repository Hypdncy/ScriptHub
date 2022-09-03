#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author:chenshifeng
@file:test_maplocal.py
@time:2020/11/29
"""
from mitmproxy import http

# script.py
from mitmproxy import http
from hacknbcb import HackNBCB
import re


def request(flow: http.HTTPFlow) -> None:
    # 将请求新增了一个查询参数
    body = flow.request.content
    print(flow.request.host)
    if "X-GW-DATA-ENCRYPT-VERSION" in flow.request.headers:
        _, new_body = HackNBCB().request_decrypt_by_common(b"", body)
        print(new_body)
        flow.request.content = new_body
    elif flow.request.host == "iib-wechat.nbcb.com.cn":
        _, new_body = HackNBCB().request_decrypt_by_comma(b"", body)
    # netloc = flow.request.headers["Host"]
    # if netloc.endswith(".nbcb.com.cn") and body:
    # flow.request.query["mitmproxy"] = "rocks"


def response(flow: http.HTTPFlow) -> None:
    # 将响应头中新增了一个自定义头字段
    pass
