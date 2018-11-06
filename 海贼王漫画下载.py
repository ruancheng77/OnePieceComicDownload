#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
海贼王漫画下载程序:
支持脚本传参或者手动指定下载剧集:
例1:
    python file_path p=1
    表示下载第一集, 下载剧集由参数 p 指定, 或者在脚本中修改 param_dict.get("p", 923) 中 param_dict 为空时的默认值
例2:
    python file_path p=10,11,12
    表示下载第 10 11 12 三集

@Author: rcddup
@Email: 410093793@qq.com
'''

import os
import re
import sys
import webbrowser

import requests
from PIL import Image

cdir = os.path.dirname(os.path.abspath(__file__))

def mkdirs(path=None, mode=0o777, exist_ok=True):
    '根据 path 创建目录'
    if not os.path.exists(path):
        os.makedirs(path, mode, exist_ok)


def clearDirs(dir):
    '清理文件目录'
    try:
        if os.path.exists(dir) and os.path.isdir(dir):
            files = os.listdir(dir)
            for file in files:
                path = os.path.join(dir, file)
                if os.path.isdir(path):
                    print("正在删除 【%s】 中的文件" % path)
                    clearDirs(path)
                else:
                    os.remove(path)
                    print('【%s】已删除。' % path)
        else:
            raise Exception('目录 [%s] 不存在或者该路径不是合法目录。' % dir)
    except Exception as e:
        print(e)


def generator(fp, pic_path_list):
    image_list = []
    image1 = Image.open(pic_path_list[0])
    pic_path_list.pop(0)
    for pic_path in pic_path_list:
        image = Image.open(pic_path)
        if image.mode == "RGBA":
            image = image.convert('RGB')
            image_list.append(image)
        else:
            image_list.append(image)
    image1.save(fp, "PDF", resolution=100.0,
                save_all=True, append_images=image_list)
    print(">>> " + fp)


def parse_arg_value(val):
    '解析参数值：将数字类型字符串转换成数字'
    m1 = re.compile(r"[+-]?[0-9]+$")
    if m1.match(val):
        return int(val)
    m2 = re.compile(r"[+-]?[0-9]+\.[0-9]+$")
    if m2.match(val):
        return float(val)
    return val


def parse_sys_argv():
    '解析参数'
    print(sys.argv)
    if len(sys.argv) > 1:
        args = sys.argv[1]
        return {kv.split("=")[0]: parse_arg_value(kv.split("=")[1]) for kv in args.split("&")}
    else:
        return {}

def produce(num):
    temp_dir = cdir + "/temp/%s" % num
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    else:
        clearDirs(temp_dir)

    pic_path_list = []

    base_url = "http://img.17dm.com/op/manhua/" + num + "/%s.png"

    # 下载漫画图片
    for i in range(1, 100):
        url = base_url % i
        resp = requests.get(url, timeout=5)
        status = resp.status_code
        if status == 404:
            break
        if resp.ok:
            fp = "%s/%s.png" % (temp_dir, i)
            pic_path_list.append(fp)
            with open(fp, "wb") as f:
                f.write(resp.content)
                print(">>> " + fp)
        else:
            print("status[%s] text[%s]" % (status, resp.text()))

    comic_path = temp_dir + "/海贼王漫画%s.pdf" % num
    # 生成 pdf
    generator(comic_path, pic_path_list)
    # 使用用户电脑默认浏览器打开 pdf
    # webbrowser.open(comic_path)


if __name__ == '__main__':
    param_dict = parse_sys_argv()
    p = str(param_dict.get("p", 923))
    ps = p.split(",")

    for num in range(ps):
        produce(num)

