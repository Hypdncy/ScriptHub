# coding:utf-8

# 解析xml，python3已经默认使用cElementTree

import xml.etree.ElementTree as ET
import argparse  # 运行前参数
import pathlib
from openpyxl import Workbook


class NmapToExcel:
    def __init__(self, infile, outfile) -> None:
        self.infile = infile
        self.outfile = outfile
        self.datas = dict()

        if not pathlib.Path(self.infile).is_file():
            print("文件不存在：{}".format(self.infile))
        else:
            self.parseXml()
            self.genXlsx()

    def parseXml(self):
        tree = ET.parse(self.infile)
        root = tree.getroot()  # 获取根节点
        xml_host_list = root.findall("host")
        for xml_host in xml_host_list:
            xml_address = xml_host.find("address")
            addr = xml_address.attrib.get('addr')
            xml_port_list = xml_host.find("ports").findall("port")
            os = xml_host.find("os")
            try:
                osmatch = os.find("osmatch")
                osName = osmatch.attrib.get("name")
                Accuracy = osmatch.attrib.get("accuracy")
            except Exception as e:
                osName = ""
                Accuracy = ""
            data = {
                "addr": addr,
                "osName": osName,
                "Accuracy": Accuracy,
                "ports": {}
            }
            for xml_port in xml_port_list:
                portId = xml_port.attrib.get('portid')
                protocol = xml_port.attrib.get('protocol')

                service = xml_port.find("service")
                serviceName = service.attrib.get('name')
                serviceProduct = service.attrib.get('product')

                data["ports"][portId] = {
                    "portId": portId,
                    "protocol": protocol,
                    "serviceName": serviceName,
                    "serviceProduct": serviceProduct,
                }

            self.datas[addr] = data

    def genXlsx(self):
        wb = Workbook()
    # 在索引为0的位置创建一个名为mytest的sheet页
        ws = wb.active
        ws.append(["地址", "系统", "系统可信度", "端口", "协议", "服务", "服务类型"])
        for addr, info in self.datas.items():
            addr = info["addr"]
            osName = info["osName"]
            Accuracy = info["Accuracy"]
            port_infos = info["ports"]
            print(port_infos)
            for portId, port_info in port_infos.items():
                print(port_info)
                protocol = port_info["protocol"]
                serviceName = port_info["serviceName"]
                serviceProduct = port_info["serviceProduct"]
                ws.append([addr, osName, Accuracy, portId,
                          protocol, serviceName, serviceProduct])

        wb.save(self.outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="xml解析")
    parser.add_argument('-x', action="store", required=False,
                        dest="xml", type=str, help='nmap result(xml file)')
    parser.add_argument('-o', action="store", required=False,
                        dest="outfile", type=str, help='outputName', default="excel.xls")
    args = parser.parse_args()
    infile = args.xml
    outfile = args.outfile
    NmapToExcel(infile, outfile)
