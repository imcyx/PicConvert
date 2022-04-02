# -*- coding: utf-8 -*-
# @Time    : 2022/1/14 18:31
# @Author  : CYX
# @Email   : im.cyx@foxmail.com
# @File    : img_convert.py
# @Software: PyCharm
# @Project : TestProject

import argparse
import os

from convert import CSDNConvert, ZHIHUConvert, BILIConvert, JIANSHUConvert
from configs import Setting_config

def get_name_list():
    """
    scan all root directory and children directory to find all markdown file
    :return: all markdown name files
    """
    name_list = []
    for files in os.listdir('./'):
        __, ext = os.path.splitext(files)
        if ext == '.md':
            name_list.append(files)
    return name_list

def handler(file, mode):
    print(f"->\t Reading file: {file}")
    with open(file, "rb") as fp:
        if mode == 'zhihu':
            converter = ZHIHUConvert()
        elif mode == 'csdn':
            converter = CSDNConvert(os.path.dirname(file))
        elif mode == 'bili':
            converter = BILIConvert(os.path.dirname(file))
        elif mode == 'jianshu':
            converter = JIANSHUConvert(os.path.dirname(file))

        res = converter.convert(fp.read().decode("utf-8"))

    new_file = os.path.basename(file)
    print(f"->\t Writing file: New_{mode}_{new_file}")
    with open(f"New_{mode}_{new_file}", "wb+") as fp2:
        fp2.write(res.encode("utf-8"))

def main():
    parser = argparse.ArgumentParser(description='This script for you to store/convert pictures between pictures bed')
    parser.add_argument('-f', default='', dest='file', type=str,
                        help='set convert markdown file (optional, default select all markdown files in root directory)')
    parser.add_argument('-m', default='', dest='mode', type=str,
                        help='set convert mode: zhihu/csdn/bili/jianshu (optional, default set in configs.py)')
    args = parser.parse_args()

    # judge which file convert
    if args.file != '':
        if os.path.exists(args.file):
            name_list = [args.file]
        else:
            raise NameError("Pls enter a correct file name!")
    else:
        name_list = get_name_list()
        print(name_list)

    # judge convert which type pic bed
    if args.mode != '':
        if args.mode in Setting_config.all_convert_modes:
            modes = [args.mode]
        else:
            raise NameError("Pls enter a correct mode!!")
    else:
        modes = Setting_config.default_mode

    # handle every markdown files
    for file in name_list:
        for mode in modes:
            handler(file, mode)

if __name__ == '__main__':
    main()