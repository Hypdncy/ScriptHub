#!/Users/hypdncy/venv/bin/python
# -*- coding: utf-8 -*-

import binascii
import base64
import hashlib
import json

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


class HackNBCB:
    '''
    header is list, append as your need
    body is string, modify as your need
    '''

    def __init__(self):
        self.key = b"F8D08904F8B8BE2D"
        self.iv = b"SHYTBASESHYTBASE"
        self.AES = AES.new(self.key, AES.MODE_CBC, self.iv)  # 创建一个aes对象
        self.data_rsa_weixin = b"T4Ue7pQnwzHupTexUsxyeDsv3Jq9sl++gmdPQ3TBvg3hvMevTIRN15m+rnGCpxttMPjuzXd9N8YiztKcp67Tiv7ldq1N02/vqKTl6qRZrrR+Mqc4ztanmkm0qEHVSFtqUfFAJojcGw7mL8GGAEN+IIJX0S82MtDWym/KqkPAmkc="
        self.data_rsa = b"YVvvelCoMU+7tgOtiF9u1ERkxhlTvJ2A/bRy4jidtMuOqZp3T0a+1mu8bXC9+ds3d04bvsH/6KXlLOdsXLnEQUm+dG6oi69ZrOX0lsNw2tvpN4k4OOXrCvU3PalYoCWVWVlXbqXRg3u+k3ILuE0szVF/MyaAIkb4F/ZVPCMNAcCEe9lJrgrlUTT72+SDl17xJoXv8xKQjRA4SgTgLTP9AKIXkNXiintxAlAjgxyv93gtKGuNZ6gRdPJHdeTRsMDa81fyu41kCZcsadleIxUq74KZEs+ckYBdjBlzDp+vFOMrjAskf1/V4Mqip/jDgii/KHaqCSo2ME0IA0SZnXX4BA=="
        self.bchar29 = chr(29).encode()

    def main(self, header, body):
        print("head:", header)
        print("body:", body)
        return header, body

    def request_encrypt_by_comma(self, header, body):
        new_body = body
        if body:
            body_pad = pad(body, 16)
            data_aes = base64.b64encode(self.AES.encrypt(body_pad))
            data_rsa = self.data_rsa
            md5 = hashlib.md5()
            md5.update(self.key + body)
            data_md5 = md5.hexdigest()
            new_body = b",".join([data_md5.encode(), data_aes, data_rsa])

        return header, new_body

    def request_decrypt_by_comma(self, header, body):
        new_body = body
        if body:
            datas = body.split(b',')
            data_md5 = datas[0]
            data_aes = datas[1]
            data_rsa = datas[2]

            new_body = self.AES.decrypt(base64.b64decode(data_aes))
        return header, new_body

    def request_encrypt_by_common(self, header, body):
        new_body = body
        if body:
            body_pad = pad(body, 16)
            data_aes = base64.b64encode(self.AES.encrypt(body_pad))
            data_rsa = self.data_rsa
            md5 = hashlib.md5()
            md5.update(self.key + body)
            data_md5 = md5.hexdigest()
            new_body = self.bchar29.join([data_md5.encode(), data_aes, data_rsa])

        return header, new_body

    def request_decrypt_by_common(self, header, body):
        new_body = body
        if body:
            datas = body.split(self.bchar29)
            data_md5 = datas[0]
            data_aes = datas[1]
            data_rsa = datas[2]

            new_body = self.AES.decrypt(base64.b64decode(data_aes))
            new_body = unpad(new_body, 16)
        return header, new_body

    def response_encrypt_by_common(self, header, body):
        new_body = body
        body_json = json.loads(str(body))
        data = body_json.get("body", None)
        if data:
            body_json["body"] = self.encrypt_by_common(data)
            new_body = json.dumps(body_json, ensure_ascii=False)
        return header, new_body

    def encrypt_by_common(self, data: str):
        data_pad = pad(data.encode(), 16)
        data_en = self.AES.encrypt(data_pad)
        data_bin = binascii.hexlify(data_en)
        confStart = b"000"
        confuseStartPos = b"000"
        confuseRule = b"00"
        confuseLen = b"000"
        originalLen = hex(len(data_bin)).replace("0x", "")
        originalLen = "{:0>6d}".format(int(originalLen)).encode()
        startData = confStart + confuseStartPos + confuseRule + confuseLen + originalLen
        return startData + data_bin

    def decrypt_by_common(self, data: str):
        encryptData = data[14:]
        confuseStartPos = int(data[3:5], 16)
        confuseLen = int(data[5:7], 16)
        confuseRule = int(data[7:8], 16)
        originalLen = int(data[8:14], 16)
        confuseData = ""
        confuseStr = encryptData[confuseStartPos: confuseStartPos + confuseLen]
        confuseStrLen = len(confuseStr)
        confuseData += encryptData[0:confuseStartPos]
        if confuseRule == 1:
            confuseData += confuseStr[confuseStrLen - 1]
            confuseData += confuseStr[1:confuseStrLen - 1]
            confuseData += confuseStr[0]
        elif confuseRule == 2:
            j = 2
            while j <= confuseStrLen:
                if j % 2 == 0:
                    confuseData += confuseStr[j - 1]
                    confuseData += confuseStr[j - 2]
                j += 1
            if confuseStrLen % 2 != 0 and confuseStrLen > 0:
                confuseData += confuseStr[confuseStrLen - 1]
        if confuseRule != 0:
            confuseData += encryptData[confuseStartPos + confuseLen:]
            encryptData = confuseData
        encryptData = encryptData[:originalLen]
        bdata = binascii.unhexlify(encryptData)
        res = self.AES.decrypt(bdata)
        new_body = unpad(res, 16)
        return new_body

    def response_decrypt_by_common(self, header, body: bytes):
        new_body = body
        body_json = json.loads(body.decode())
        data = body_json.get("body", None)
        if data:
            # data_body = self.decrypt_by_common(data).decode()
            # data_json = json.loads(data_body)
            # print(body_json["body"])
            # body_json["body"] = data_json

            body_json["body"] = self.decrypt_by_common(data).decode()
            print(body_json["body"])
            new_body = json.dumps(body_json, ensure_ascii=False).encode()
        return header, new_body


if __name__ == "__main__":
    data = b'F8D08904F8B8BE2D{"LOGIN_ID":"18248487654","DEVICE_FINGER":"j0JXxzJLZYgx0icoDH5I_8GiPlYxNDiIC1j1eiR81IhAqnoY89LSkBs0gZcdhGGCjBKWczuQ0a432wagIXrJHmm2wYMbhz-hwAU1kgL0upySNcjd2dVYVqBMm6Zx6neNOV7oFEQUlmE-UlCQoelhV56cJ0DFIVKT","CLIENT_TYPE":"WB","CLIENT_OS":"W","isWebPage":true,"REQ_TIME":"20220622182248498"}'

    res = hashlib.md5(data).hexdigest()
    print(res)
    pass
