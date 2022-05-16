# -*- coding: utf-8 -*-

import oss2

endpoint = 'http://oss-cn-hangzhou-zwynet-d01-a.internet.cloud.zj.gov.cn' # Suppose that your bucket is in the Hangzhou region.

auth = oss2.Auth('95TW0ZUOpye6TQBz', 'dL3RHAGhB1+dzG5wN7Y8Y8rC5dI=')
bucket = oss2.Bucket(auth, endpoint, 'szjg-oss')

# # The object key in the bucket is story.txt
# key = 'story.txt'
#
# # Upload
# bucket.put_object(key, 'Ali Baba is a happy youth.')
#
# # Download
# bucket.get_object(key).read()
#
# # Delete
# bucket.delete_object(key)

# Traverse all objects in the bucket
for object_info in oss2.ObjectIterator(bucket):
    print(object_info.key)