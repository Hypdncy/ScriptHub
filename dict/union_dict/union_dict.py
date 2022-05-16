import pathlib
from pathlib import Path
from config.setting import *


def merge_dict_to_dirsearch():
    if not Path(FILE_dirsearch_dicc).is_file():
        raise "文件FILE_dirsearch_dicc不存在"

    print(Path(".").resolve())
    files = Path("./srcdicts/").rglob("*")
    dics = set([])
    for file in files:
        if file.name in [".", ".."]:
            continue
        with open(file, 'r') as f:
            lines = f.readlines()
            lines = [line.strip() for line in lines]
            dics.update(lines)

    print(len(dics))
    with open(Path(FILE_dirsearch_dicc), 'r') as f:
        lines = f.readlines()
        l_old_dicc = [line.strip() for line in lines]
    print("源来数量{}".format(len(l_old_dicc)))
    dics.update(l_old_dicc)
    print("最新数量{}".format(len(dics)))
    print("新增数量{}".format(len(dics) - len(l_old_dicc)))
    l_dics = list(dics)
    l_dics.sort()
    with open(Path(FILE_dirsearch_dicc), 'w') as f:
        f.writelines([dic + '\n' for dic in l_dics])


if __name__ == "__main__":
    merge_dict_to_dirsearch()
