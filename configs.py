# -*- coding: utf-8 -*-
# @Time    : 2022/3/30 14:08
# @Author  : CYX
# @Email   : im.cyx@foxmail.com
# @File    : configs.py
# @Software: PyCharm
# @Project : PicConvert


import json
import os
import sys

path = os.path.join(os.path.split(os.path.abspath(sys.argv[0]))[0], "cookies.json")

''' loading json file '''
with open(path, 'r') as fp:
    dicts = json.loads(fp.read())

""" include 4 modes, choose 1~4 as default mode(s) """
default_modes = dicts['default_modes']
total_modes = dicts['total_modes']

class Setting_config(object):
    """
        User can set your own parameters here
    """

    ''' config extensions which will be detected as pattern '''
    ''' (Warning!! some websites cannot support all extensions below) '''
    ext = ['png', 'bmp', 'jpg', 'jpeg', 'gif']
    pattern = ''.join(']\(?.*\.' + i + '\)|' + '="+.*\.' + i + '"|' for i in ext)[:-1]

    # csdn img-bed config
    csdn_cookies = dicts['csdn_cookies']
    # bilibili img-bed config
    bili_cookies = dicts['bili_cookies']
    # jianshu img-bed config
    jianshu_cookies = dicts['jianshu_cookies']
    # bokeyuan img-bed config
    bokeyuan_cookies = dicts['bokeyuan_cookies']
    # zhihu img-bed config
    zhihu_cookies = dicts['zhihu_cookies']
    # zhihu convert status (src, watermark_src, original_src)
    zhihu_mode = "original_src"


class CSDN_config(Setting_config):
    cookies = Setting_config.csdn_cookies

    up_headers = {
        'x-image-app': 'direct_blog',
        'x-image-dir': 'direct'
    }
    up_url = "https://imgservice.csdn.net/direct/v1.0/image/upload?watermark=&type=blog&rtype=markdown"

    boundary = '----WebKitFormBoundaryKzs0YGpR02NCBive'
    path_headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }
    path_url = "https://csdn-img-blog.oss-cn-beijing.aliyuncs.com/"

    fields = {'art_id': 'undefined'}
    cookies['UserInfo'] = cookies['UserToken']
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "content-type": "application/json"
    }
    convert_url = "https://imgservice.csdn.net/img-convert/external/storage"

class ZHIHU_config(Setting_config):
    cookies = Setting_config.zhihu_cookies
    mode = Setting_config.zhihu_mode

    boundary = '----WebKitFormBoundaryA7rHHPjs3umheW1O'
    headers = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
        "referer": "https://zhuanlan.zhihu.com/write",
        "origin": "https://zhuanlan.zhihu.com",
        "x-requested-with": "fetch",
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }
    mode_dict = ['src', 'watermark_src', 'original_src']
    fields = {'source': 'article'}
    convert_url = "https://zhuanlan.zhihu.com/api/uploaded_images"

class BILI_config(Setting_config):
    cookies = Setting_config.bili_cookies

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "referer": "https://member.bilibili.com/",
        "origin": "https://member.bilibili.com",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    b64_head = 'data:image;base64,'
    fields = {'csrf': cookies['bili_jct']}
    convert_url = "https://api.bilibili.com/x/article/creative/article/upcover"

class JIANSHU_config(Setting_config):
    cookies = Setting_config.jianshu_cookies

    boundary = '------WebKitFormBoundaryoDKCqoQaipUHiBdS'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
        "Host": "upload.qiniup.com",
        "Origin": "https://www.jianshu.com",
        "Referer": "https://www.jianshu.com/",
        "content-type": f"multipart/form-data; boundary={boundary}",
        "Sec-Fetch-Dest": "empty"
    }
    token_url = "https://www.jianshu.com/upload_images/token.json?filename=image."
    convert_url = "https://upload.qiniup.com/"

class BOKEYUAN_config(Setting_config):
    cookies = Setting_config.bokeyuan_cookies

    boundary = '----WebKitFormBoundary0YtEgqslRTAf1lEB'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "origin": "https://i.cnblogs.com",
        "referer": "https://i.cnblogs.com/",
        "content-type": f"multipart/form-data; boundary={boundary}",
        'x-xsrf-token': 'CfDJ8AuMt_3FvyxIgNOR82PHE4mor62BfuI58rIEHB4fHCfGnPXDShqSPjlPtYED-W3kcbAFy0VuhQU0xFNDVgbXQb_603YRMn_Mp9RbW9NkTV9pxpK8Yz3FQ0Oh9fw5jTMrmQZUZICAjUyRZVBgJ9H9zfpYW-QlLgVF6iJeJfR7ojwvT8QyU536rfXsAPFTUbL_xQ',
    }
    fields = {'host': 'www.cnblogs.com', 'uploadType': 'Paste'}
    convert_url = "https://upload.cnblogs.com/imageuploader/CorsUpload/"