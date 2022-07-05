import multiprocessing
import pathlib
import time
from Crypto.Cipher import ARC4
import re

goble_len = 1024 * 1024 * 2


class RC4UTIL():
    def __init__(self, key):
        if isinstance(key, str):
            self.__keyGen = key.encode()
        elif isinstance(key, bytes):
            self.__keyGen = key

    def encrypt(self, data) -> bytes:
        rc4 = ARC4.new(self.__keyGen)
        res = rc4.encrypt(data)
        return res

    def decrypt(self, data) -> bytes:
        rc4 = ARC4.new(self.__keyGen)
        res = rc4.decrypt(data)
        # res = base64.b64encode(res)
        return res


def get_rc4_key():
    guid_dir = r"C:\Users\Administrator\AppData\Roaming"
    guid_files = pathlib.Path(guid_dir).iterdir()
    guid_txts = []
    for guid_file in guid_files:
        if guid_file.name.endswith("-RSA.txt"):
            with open(guid_file, 'r') as f:
                guid_txts.append(f.read())
            print("guid_file:{}".format(guid_file.resolve()))
            print("guid_content:{}".format(guid_txts[0]))
            break

    if not guid_txts:
        raise "没有发现GUID-RSA.txt"
    # return guid_txts[0]
    guid_txt = guid_txts[0]
    text0 = guid_txt[0]
    texte = guid_txt[-1]
    text_0 = guid_txt.split('-')[0]

    def pad(text):
        while len(text) % 8 != 0:  # 不是8的倍数，用空格补全成8的倍数
            text += ' '
        return text

    text_numbers = re.findall(r'[0-9]+', text_0)
    text_number = "".join(text_numbers)
    text3 = "{}{}{}".format(text0, text_number, texte)
    print("text:{}".format(text3))
    import subprocess

    proc = subprocess.Popen(["3des.exe", text3], shell=True,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outs, errs = proc.communicate(timeout=5)
    res = outs.decode().strip()
    if not res:
        raise "加密错误"

    text_3des = res

    text_3des = text_3des.replace("+", "").replace("=", "").replace("/", "")
    text_3des_0 = text_3des[:4]
    text_3des_1 = text_3des[-4:]
    text_rc4_key = text_3des_0 + text_3des_1
    print("text_rc4_key:{}".format(text_rc4_key))

    return text_rc4_key


goble_key = get_rc4_key()
gpble_flag = "coffee." + goble_key[:4]


def scan_disk(disk_path):
    disk_pathlib = pathlib.Path(disk_path)
    # encrypt_fils = disk_pathlib.rglob(
    #     "*.{gpble_flag}.*".format(gpble_flag=gpble_flag))
    encrypt_fils = disk_pathlib.rglob(
        "请阅读我.RSA.txt")
    count = 0
    for encrypt_file in encrypt_fils:
        if not encrypt_file.is_file():
            continue
        file_name = encrypt_file.name

        try:
            encrypt_file.unlink()
            count += 1
        except Exception:
            print("错误:{}".format(file_name))

    print("完成{}:{}".format(disk_path, count))


if __name__ == "__main__":
    s = time.time()
    process = []
    # F盘开始
    # for disk in range(70, 91):
    for disk in range(65, 91):

        disk = chr(disk)
        # if disk=="C":
        #     disk="C:\\Users"
        disk_path = pathlib.Path("{}:\\".format(disk))
        if str(disk_path.resolve()).startswith("C"):
            disk_path = pathlib.Path(pathlib.PurePath(disk_path, "Users"))

        process.append(multiprocessing.Process(
            target=scan_disk, args=(disk_path,)))
    # process.reverse()
    for p in process:
        p.start()
    for p in process:
        p.join()
    e = time.time()
    print(e - s)

    scan_disk("C:\\ProgramData")
    scan_disk("C:\\Python32")
    scan_disk("C:\\AMD")
    scan_disk("C:\\kingsoft")