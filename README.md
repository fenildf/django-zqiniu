# django-qiniu

在Django中集成七牛服务

这里完整实现了`django.core.files.storage.Storage`。在任何需要使用七牛服务的地方都可以使用本类。


## 安装

`pip install django-zqiniu`


## 配置

在`settings.py`中增加以下配置：
```
QINIU_SETTINGS = {
    'ACCESS_KEY': 'your access_key',
    'SECRET_KEY': 'your secret_key',
    # 如果不是手动创建QiniuStorage的实例，Django会使用默认的Bucket
    'DEFAULT_BUCKET': 'your default bucket',
    # Bucket配置，key为任意字符串
    'BUCKET_CONFIGS': {
        'your default bucket': {
            'BUCKET_NAME': 'test',
            'BUCKET_URL': 'http://oce67vkmg.bkt.clouddn.com',
            # 如果没有配置自定义域名，留空即可，默认值: ''
            'BIND_URL': 'http://img.chayoulun.com',
            # 默认值: ''
            'PREFIX': '',
            # 私有空间还是公有空间？，默认值: False
            'IS_PRIVATE': False,
            # 私有链接的有效时间，单位秒，默认值: 3600
            'EXPIRES': 3600,
        },

        ...
    }
}
```


## 使用

1. 将`djang_zqiniu.storage.QiniuStorage`作为默认Storage。

    修改settings.py：

    `DEFAULT_FILE_STORAGE = 'djang_zqiniu.storage.QiniuStorage'`

2. 或者仅仅在需要的地方使用实例

```python

from django.db import models

from djang_zqiniu.storage import QiniuStorage

# 确保 'your default bucket'存在于配置中
qiniu_storage = QiniuStorage('your default bucket')


class SomeModel(models.Model):

    uploaded_file = models.FileField(storage=qiniu_storage)
```
