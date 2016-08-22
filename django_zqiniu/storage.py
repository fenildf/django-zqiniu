#-*- coding:utf-8 -*-
import os
from django.conf import settings
from django.utils.deconstruct import deconstructible
from django.core.files import File
from django.core.files.storage import Storage

from qiniu import Auth, BucketManager, put_file


@deconstructible
class QiniuStorage(Storage):
    '''
    七牛存储
    '''

    def __init__(self, access_key=None, secret_key=None, bucket=None, prefix=''):
        self.access_key = access_key or settings.QINIU_DEFAULT_ACCESS_KEY
        self.secret_key = secret_key or settings.QINIU_DEFAULT_SECRET_KEY
        self.bucket_name = bucket or settings.QINIU_DEFAULT_BUCKET_NAME
        self.bucket_url = bucket or settings.QINIU_DEFAULT_BUCKET_URL
        self.prefix = prefix or settings.QINIU_DEFAULT_PREFIX

        self.__auth = Auth(self.access_key, self.secret_key)
        self.__bucket = BucketManager(self.__auth)

    def delete(self, name):
        '''
        TODO: name不存在
        '''
        if self.exists(name):
            bucket.delete(bucket_name, self.prefix + name)

    def exists(self, name):
        ret, info = self.__bucket.stat(self.bucket_name, self.prefix + name)
        return 'hash' in ret

    def path(self, name):
        return self.prefix + name

    def listdir(self, prefix):
        if not prefix:
            prefix = self.prefix
        ret, eof, info = self.__bucket.list(self.bucket_name, prefix=prefix)
        return ret

    def size(self, name):
        ret, info = self.__bucket.stat(self.bucket_name, self.prefix + name)
        return ret['fsize']

    def url(self):
        return urljoin(self.bucket_url, self.path(name))

    def put_time(self, name):
        ret, info = self.__bucket.stat(self.bucket_name, self.prefix + name)
        return ret['putTime']

    def save(self, name, content, max_length=None):
        file_name = os.path.basename(name)
        token = self.__auth.upload_token(self.bucket_name, self.path(file_name), -1)
        ret, info = put_file(token, self.path(file_name), name)
        return self.path(file_name)

    def __eq__(self, other):
        return [
            self.access_key == other.access_key,
            self.secret_key == other.secret_key,
            self.bucket_name == other.bucket_name,
            self.prefix == other.prefix,
        ]
