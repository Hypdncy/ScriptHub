import base64
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex


## 先encode是为了防止明文有中文报错, 中文utf8编码后是占3个字节<gbk编码是占2个字节>, 数字和字母是占1个字节

# 填充函数
def add_to_16(value):
    while len(value.encode('utf-8')) % 16 != 0:
        value += '\x00'  # 补全, 明文和key都必须是16的倍数
    return value.encode('utf-8')


# 加密
def AESEncrypt():
    text = 'ilvoelove我爱你呀'
    iv = '0123456789ABCDEF'
    key = '123456789qwertyu'
    aes = AES.new(key=add_to_16(key), mode=AES.MODE_CBC, iv=iv.encode())
    encryptedstr = aes.encrypt(add_to_16(text))  # 加密后得到的字节数据
    # 结果: b'\x8f#\x10\xeb\xf8\x13\xb4\xb5\x11\x9d\x185'
    en_str = base64.b64encode(encryptedstr).decode()  # 以base64编码方式解码, 得到加密字符串!
    # 结果:yMQ6/gTtLURnRg1Iu2ZMiix79u8jsVHHFA2qKs28aQ=
    # en_str = b2a_hex(encryptedstr).decode()  # 以hex编码方式解码, 得到加密字符串
    # 结果:8f2310ebf813b4b5119d183522ed993228b1efdbbc8ec5471c5036a8ab36f1a4
    return en_str  # 把加密后的字节数据返回


# 解密
def AESDecrypt(en_str):
    iv = '0123456789ABCDEF'
    key = '123456789qwertyu'
    # 解密时必须重新构建aes对象
    aes = AES.new(key=add_to_16(key), mode=AES.MODE_CBC, iv=iv.encode())
    # 先把密文转换成字节型, 再解密, 最后把之前填充的'\x00' 去掉
    decryptedstr = aes.decrypt(base64.decodebytes(en_str)).decode().strip('\x00')
    # decryptedstr = aes.decrypt(a2b_hex(en_str)).decode().strip('\x00') # 对应上面的hex编码
    print(decryptedstr)


if __name__ == '__main__':
    en_str = AESEncrypt()
    AESDecrypt(en_str)

