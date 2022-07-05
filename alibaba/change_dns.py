from urllib.request import urlopen
from json import load
from dnsParse.dns_parse import DNSParse


def get_ipaddress_1():
    try:
        my_ip = load(urlopen('http://httpbin.org/ip', timeout=10))['origin']
        return my_ip
    except Exception as e:
        return ""


def get_ipaddress_2():
    try:
        my_ip = load(urlopen('http://jsonip.com'))['ip']
        return my_ip
    except Exception as e:
        return ""


def get_ipaddress_3():
    try:
        my_ip = load(urlopen('https://api.ipify.org/?format=json'))['ip']
        return my_ip
    except Exception as e:
        return ""


if __name__ == '__main__':
    ipaddress = ""
    funcs = [get_ipaddress_1, get_ipaddress_2, get_ipaddress_3]
    for func in funcs:
        ipaddress = func()
        with open("/etc/cron.10min/ip.txt", "r") as f:
            datas = f.read()
            lines = datas.strip().splitlines()
            old_ipaddress = lines[-1] if lines else ""
        if ipaddress != old_ipaddress:
            DNSParse().main(ipaddress)
            lines.append(ipaddress)
            with open("./ip.txt", "w") as f:
                new_lines = [line + "\n" for line in lines]
                f.writelines(new_lines)