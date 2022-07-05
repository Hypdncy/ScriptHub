# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import sys

from typing import List

from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class DNSParse:
    def __init__(self):
        pass

    @staticmethod
    def create_client(access_key_id: str, access_key_secret: str) -> Alidns20150109Client:
        """
        使用AK&SK初始化账号Client
        @param access_key_id:
        @param access_key_secret:
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config(
            # 您的 AccessKey ID,
            access_key_id=access_key_id,
            # 您的 AccessKey Secret,
            access_key_secret=access_key_secret
        )
        # 访问的域名
        config.endpoint = f'alidns.cn-hangzhou.aliyuncs.com'
        return Alidns20150109Client(config)

    @staticmethod
    def main(ipaddress: str) -> None:
        client = DNSParse.create_client('LTAI5tJaQqoju4e6QJvNDARh', 'k9OUwFtUMM2i3nGr0aH1bYp7aWDCZh')
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            record_id='771979896587652096',
            lang='Python',
            rr='root-home',
            type='A',
            value=ipaddress
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            client.update_domain_record_with_options(
                update_domain_record_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error)
            raise error

    @staticmethod
    async def main_async(args: List[str], ) -> None:
        client = DNSParse.create_client('LTAI5tJaQqoju4e6QJvNDARh', 'k9OUwFtUMM2i3nGr0aH1bYp7aWDCZh')
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            lang='Python',
            rr='www',
            type='A',
            value='127.0.0.3'
        )
        runtime = util_models.RuntimeOptions()
        try:
            # 复制代码运行请自行打印 API 的返回值
            await client.update_domain_record_with_options_async(update_domain_record_request, runtime)
        except Exception as error:
            # 如有需要，请打印 error
            UtilClient.assert_as_string(error)


if __name__ == '__main__':
    pass
    # DNSParse.main("")
