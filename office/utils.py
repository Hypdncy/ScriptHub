import os
from win32com import client as wc
import time
import pathlib

#  注意：目录的格式必须写成双反斜杠
doc_dir = "C:\\Users\\wbl\\Desktop\\pythonProject1\\"  # 使用绝对地址（可更改）
doc_files = pathlib.Path(doc_dir).rglob('*.doc')
if doc_files:
    pathlib.Path(pathlib.PurePath(doc_dir, "docx")).mkdir(parents=True, exist_ok=True)
for file in doc_files:
    # 找出文件中以.doc结尾并且不以~$开头的文件（~$是为了排除临时文件）
    if file.name.startswith('~$'):
        continue
    word = wc.Dispatch("Word.Application")
    print("已处理文件：" + str(file.resolve()))
    # 打开文件
    doc = word.Documents.Open()
    # 将文件另存为.docx
    doc.SaveAs("./docx/{}x".format(file.resolve()), 16)  # 12表示docx格式
    doc.Close()

    word.Quit()
    time.sleep(0.5)  # 暂停0.5秒
