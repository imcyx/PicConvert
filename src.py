# -*- coding: utf-8 -*-
# @Time    : 2022/3/30 22:12
# @Author  : CYX
# @Email   : im.cyx@foxmail.com
# @File    : src.py
# @Software: PyCharm
# @Project : PicConvert

import os
import re
import json
import time
import uuid
import base64
import requests
from io import BytesIO
from requests_toolbelt.multipart.encoder import MultipartEncoder

from configs import CSDN_config, ZHIHU_config, BILI_config, JIANSHU_config, BOKEYUAN_config, Setting_config


class CSDNConvert(CSDN_config):
    """
    CSDN convert apply
    """
    def __init__(self, root):
        self.root = root

        def get_short_id():
            """
            get a uuid form array
            :return: uuid form short id
            """
            # support .jpg .gif .png .jpeg .bmp .webp, size less than 5 Mb
            array = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                     "s", "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                     "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                     "S", "T", "U", "V", "W", "X", "Y", "Z"]
            id_str = str(uuid.uuid4()).replace("-", '')
            buffer = []

            for i in range(0, 8):
                start = i * 4
                end = i * 4 + 4
                val = int(id_str[start:end], 16)
                buffer.append(array[val % 62])

            return "".join(buffer)

        self.fields.update({'uuid': 'img-' + get_short_id() + '-' + str(round(time.time() * 1000))})

    def convert(self, src):
        # convert address
        if src.find('http') >= 0:
            self.fields.update({'imgUrl': src})
            payload = json.dumps(self.fields)
            res = requests.post(self.convert_url, data=payload, cookies=self.cookies, headers=self.headers)
        # upload imgs and get address
        else:
            self.up_headers['x-image-suffix'] = src.split('.')[-1]
            up_res = requests.get(self.up_url, cookies=self.cookies, headers=self.up_headers).json()
            # if request legal
            if up_res['code'] != 200:
                raise Exception(up_res['msg'])

            up_res = up_res['data']
            data = {
                'key': up_res['filePath'],
                'policy': up_res['policy'],
                'OSSAccessKeyId': up_res['accessId'],
                'signature': up_res['signature'],
                'callback': up_res['callbackUrl'],
                'file': open(os.path.join(self.root, src), 'rb').read()
            }
            multipart_encoder = MultipartEncoder(fields=data, boundary=self.boundary)
            res = requests.post(self.path_url, data=multipart_encoder, cookies=self.cookies, headers=self.path_headers)

        # if request legal
        if res.json()['code'] != 200:
            raise Exception(res.json()['msg'])
        res_url = res.json()['data']['url'] if src.find('http') >= 0 else res.json()['data']['imageUrl']

        return res_url

class ZHIHUConvert(ZHIHU_config):
    """
    ZHIHU convert apply
    """
    def __init__(self):
        if self.mode not in self.mode_dict:
            raise Exception(" You enter a not support picture mode!")

    def convert(self, src):
        self.fields['url'] = src
        multipart_encoder = MultipartEncoder(fields=self.fields, boundary=self.boundary)
        res = requests.post(self.convert_url, data=multipart_encoder, cookies=self.cookies, headers=self.headers)

        # if request legal
        if res.status_code != 200:
            raise Exception(res.json()['error']['message'])
        res_url = res.json()[self.mode]

        return res_url

class BILIConvert(BILI_config):
    def __init__(self, root):
        self.root = root

    def convert(self, src):
        # concat data
        if src.find('http') >= 0:
            content = BytesIO(requests.get(src).content).read()
        else:
            content = open(os.path.join(self.root, src), 'rb').read()
        self.fields['cover'] = self.b64_head + str(base64.b64encode(content))[2:-1]

        res = requests.post(self.convert_url, data=self.fields, cookies=self.cookies, headers=self.headers)
        # if request legal
        if res.json()['code'] != 0:
            raise TypeError(res.json()['message'])
        res_url = res.json()['data']['url']

        return res_url

class JIANSHUConvert(JIANSHU_config):
    def __init__(self, root):
        self.root = root
        requests.get('https://www.jianshu.com/', cookies=self.cookies)

    def convert(self, src):
        # concat data
        payload = requests.get(self.token_url + src.split('.')[-1], headers=self.headers, cookies=self.cookies).json()

        if src.find('http') >= 0:
            payload['file'] = requests.get(src, headers=self.headers).content
        else:
            payload['file'] = open(os.path.join(self.root, src), 'rb').read()
        payload['x:protocol'] = 'https'
        multipart_encoder = MultipartEncoder(fields=payload, boundary=self.boundary)

        # request
        res = requests.post(self.convert_url, data=multipart_encoder, headers=self.headers)
        # if request legal
        if res.status_code != 200:
            raise Exception(res.json()['error'])
        res_url = res.json()['url']

        return res_url

class BOKEYUANConvert(BOKEYUAN_config):
    def __init__(self, root):
        self.root = root

    def convert(self, src):
        # concat data
        if src.find('http') >= 0:
            self.fields['imageFile'] = (src, requests.get(src).content, 'image/png')
        else:
            self.fields['imageFile'] = (src, open(os.path.join(self.root, src), 'rb').read(), 'image/png')
        multipart_encoder = MultipartEncoder(fields=self.fields, boundary=self.boundary)

        # request
        requests.options(self.convert_url)
        res = requests.post(self.convert_url, data=multipart_encoder, headers=self.headers, cookies=self.cookies)

        if not res.json()['success']:
            raise Exception(res.json()['message'])

        # if request legal
        res_url = res.json()['message']
        return res_url

def img_convert(mode, text, root, link=False):
    if mode == 'zhihu':
        handle = ZHIHUConvert()
    elif mode == 'csdn':
        handle = CSDNConvert(root)
    elif mode == 'bili':
        handle = BILIConvert(root)
    elif mode == 'jianshu':
        handle = JIANSHUConvert(root)
    elif mode == 'bokeyuan':
        handle = BOKEYUANConvert(root)

    if link:
        res_url = handle.convert(text)
        # if get available convert address
        if res_url:
            print(f"-> {res_url}")
        else:
            raise Exception('Convert false!')
        return res_url

    else:
        res_text = ''
        last_end = 0
        for query in re.finditer(Setting_config.pattern, text, re.I):
            src = query.group()[2:-1]
            print(f"{src}", end=' ')
            res_url = handle.convert(src)
            # if get available convert address
            if res_url:
                print(f"-> {res_url}")
            else:
                raise Exception('Convert false!')
            # change source file, then do another search
            res_text += text[last_end:query.start() + 2] + res_url
            last_end = query.end() - 1
        res_text += text[last_end:]

        return res_text
