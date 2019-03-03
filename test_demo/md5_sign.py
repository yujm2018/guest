# -*- coding: utf-8 -*-
# @Time     : 2018/3/4 16:04
# @Author   : yujianming
# @File     : md5_sign.py
# @Software : PyCharm Community Edition
import hashlib

md5 = hashlib.md5()
sign_str = "@admin123"
sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
md5.update(sign_bytes_utf8)
sign_md5 = md5.hexdigest()
print(sign_md5)