# -*- coding: utf-8 -*-
# @Time    : 2022/3/30 14:08
# @Author  : CYX
# @Email   : im.cyx@foxmail.com
# @File    : configs.py
# @Software: PyCharm
# @Project : try


class Setting_config(object):
    """
        User can set your own parameters here
    """

    ''' config extensions which will be detected as pattern '''
    ''' (Warning: some websites cannot support all extensions below) '''
    ext = ['png', 'bmp', 'jpg', 'jpeg', 'jpe', 'jfif', 'gif', 'tif', 'dib', 'webp', 'ico']

    ''' include 4 modes, choose 1~4 as default mode(s) '''
    default_mode = ['bili']
    all_convert_modes = ['zhihu', 'csdn', 'bili', 'jianshu']

    ''' csdn img-bed config '''
    csdn_cookies = {
        "UserName": "qq_42059060",
        "UserToken": "b6b8fd30627d4c639b6f0d619841f39a",
    }

    ''' zhihu img-bed config '''
    zhihu_cookies = {
        "z_c0": '"2|1:0|10:1648889311|4:z_c0|92:Mi4xcEZuTkNBQUFBQUFBSUozTmRKcTRFeWNBQUFDRUFsVk4zcHB2WWdCMXJJNWREcG9KNU5vNXFVU1pqRGhTWFh6Zmt3|e8a9e1846f8c55a976a3a269d924d26a83feb9562835bf4a850399004a818358"',
    }
    # choose pictures convert status in zhihu (src, watermark_src, original_src)
    zhihu_mode = "original_src"

    ''' bilibili img-bed config '''
    bili_cookies = {
        'SESSDATA': '92c1ec7f%2C1649473981%2Cb03b3*a1'
    }

    ''' jianshu img-bed config'''
    jianshu_cookies = {
        '_m7e_session_core': '5b69abcac7daf4cb25f3926723bdef38'
    }


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

    pattern = ''.join(']\(?.*\.' + i + '\)|' for i in Setting_config.ext)[:-1]

class ZHIHU_config(Setting_config):
    cookies = Setting_config.zhihu_cookies
    mode = Setting_config.zhihu_mode

    boundary = '----WebKitFormBoundaryA7rHHPjs3umheW1O'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "referer": "https://zhuanlan.zhihu.com/write",
        "origin": "https://zhuanlan.zhihu.com",
        "x-requested-with": "fetch",
        "Content-Type": f"multipart/form-data; boundary={boundary}"
    }
    mode_dict = ['src', 'watermark_src', 'original_src']
    fields = {'source': 'article'}
    convert_url = "https://zhuanlan.zhihu.com/api/uploaded_images"
    pattern = ''.join(']\(?.*\.' + i + '\)|' for i in Setting_config.ext)[:-1]

class BILI_config(Setting_config):
    cookies = Setting_config.bili_cookies

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "referer": "https://member.bilibili.com/",
        "origin": "https://member.bilibili.com",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    b64_head = 'data:image;base64,'
    fields = {'csrf': 'c109546c087f7d2f45f48e365c96e91e'}
    cookies['bili_jct'] = 'c109546c087f7d2f45f48e365c96e91e'
    convert_url = "https://api.bilibili.com/x/article/creative/article/upcover"
    pattern = ''.join(']\(?.*\.' + i + '\)|' for i in Setting_config.ext)[:-1]

class JIANSHU_config(Setting_config):
    cookies = Setting_config.jianshu_cookies

    boundary = '----WebKitFormBoundaryEjkSZUASM1SA9AKn'
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
        "Host": "www.jianshu.com",
        "Referer": "https://www.jianshu.com/writer",
        "content-type": f"multipart/form-data; boundary={boundary}",
    }
    token_url = "https://www.jianshu.com/upload_images/token.json?filename=image."
    convert_url = "https://upload.qiniup.com/"
    pattern = ''.join(']\(?.*\.' + i + '\)|' for i in Setting_config.ext)[:-1]