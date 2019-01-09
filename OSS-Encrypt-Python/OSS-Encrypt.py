# -*- coding: utf-8 -*-

import os
import shutil

import oss2


access_key_id = os.getenv('OSS_TEST_ACCESS_KEY_ID', '<Your AccessKeyId>')
access_key_secret = os.getenv('OSS_TEST_ACCESS_KEY_SECRET', '<Your AccessKeySecret>')
bucket_name = os.getenv('OSS_TEST_BUCKET', '<Your Bucket>')
endpoint = os.getenv('OSS_TEST_ENDPOINT', 'http://oss-ap-northeast-1.aliyuncs.com')


# Bucketを作成する
bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)


# Objectを作成する。暗号化するためにKMSを指定する。
bucket.put_object('motto.txt', 'Never give up. - Jack Ma', headers={"x-oss-server-side-encryption" : "KMS"})