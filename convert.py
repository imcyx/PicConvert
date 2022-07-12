# -*- coding: utf-8 -*-
# @Time    : 2022/1/14 18:31
# @Author  : CYX
# @Email   : im.cyx@foxmail.com
# @File    : convert.py
# @Software: PyCharm
# @Project : PicConvert

import argparse
import os

from src import img_convert
from configs import default_modes, total_modes

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

def handler(file, mode, link=False):
    if link:
        res = []
        for f in file:
            print(f)
            res.append(img_convert(mode, f, os.path.dirname(f), link=True))
        print("Upload Success:")
        print('\n'.join(res))
    else:
        print(f"Reading File: {file}")
        print("-"*50)
        with open(file, "rb") as fp:
            res = img_convert(mode, fp.read().decode("utf-8"), os.path.dirname(file))

        new_file = f'New_{mode}_{os.path.basename(file)}'
        print("-"*50)
        print(f"Writing File: {new_file}\n")
        with open(new_file, "wb+") as fp2:
            fp2.write(res.encode("utf-8"))

def main():
    parser = argparse.ArgumentParser(description='This script for you to store/convert pictures between pictures bed')
    parser.add_argument('-f', default='', dest='file', type=str,
                        help='set convert markdown file (optional, default select all markdown files in root directory)')
    parser.add_argument('-m', default='', dest='mode', type=str,
                        help='set convert mode: zhihu/csdn/bili/jianshu (optional, default set in configs.py)')
    parser.add_argument('-d', default='', dest='direct', type=str, nargs='+',
                        help='directly convert')
    args = parser.parse_args()

    # judge convert which type pic bed
    if args.mode != '':
        if args.mode in total_modes:
            modes = [args.mode]
        else:
            raise NameError("Pls enter a correct mode!!")
    else:
        modes = default_modes

    # if direct convert links/img_files
    if args.direct:
        name_list = args.direct
        for mode in modes:
            handler(name_list, mode, link=True)

    # if convert files
    else:
        # judge which file convert
        if args.file != '':
            if os.path.exists(args.file):
                name_list = [args.file]
            else:
                raise NameError("Pls enter a correct file name!")
        else:
            name_list = get_name_list()
            if not name_list:
                raise Exception('Markdown files not found!')

        print(f"\nFiles: {'  '.join(name_list)}", f"\nModes: {'  '.join(modes)}", '\n')

        # handle every markdown files or every links/img_files
        for file in name_list:
            for mode in modes:
                handler(file, mode)

if __name__ == '__main__':
    main()