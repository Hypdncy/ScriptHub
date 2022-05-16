from IPy import IP


def get_ips_by_mask(ip, mask):
    l_ips = []
    try:
        ips = IP(ip).make_net(mask)
        for ip in ips:
            if ip.iptype() == 'PUBLIC':
                l_ips.append(ip.strNormal())
        # l_ips = [ for ip in ips]
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


if __name__ == "__main__":
    mask = 29
    from_file = "./ips.txt"
    to_file = "./ips-{}.txt".format(mask)
    get_ips_from_file_to_file(from_file, to_file, mask)
    # get_ips_by_mask("192.168.11.0", 30)
