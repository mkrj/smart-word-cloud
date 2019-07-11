# -*- coding:utf-8 -*-
import os
import zipfile
import rfc6266
import time

from flask import make_response, send_file


def is_number(word):
    try:
        _ = int(word)
    except ValueError:
        return False
    return True


def zip_files(files):
    """
    将多个文件，打包成zip文件，同时删除已经打包的文件
    :param files: list类型，待压缩的文件
    :return: 压缩后生成文件的路径
    """
    # 设置压缩文件存放路径
    if len(files) < 1:
        raise Exception('Get no files to zip.')

    saved_dir = os.path.split(files[0])[0]
    zip_name = str(int(time.time())) + '.zip'
    zip_file_path = os.path.join(saved_dir, zip_name)

    # 开始压缩文件
    z = zipfile.ZipFile(zip_file_path, 'w')
    try:
        for file in files:
            arcname = os.path.split(file)[1]  # 只把文件放入压缩包，不含文件父级文件夹
            z.write(file, arcname=arcname)
    finally:
        z.close()

    for file in files:
        os.remove(file)

    return zip_file_path


def to_response(real_file, final_filename):
    """
    返回生成的文件
    :param real_file: str类型,文件路径
    :param final_filename: str类型,显示在前端的文件名字
    """
    response = make_response(send_file(real_file))

    response.headers['Content-Disposition'] = rfc6266.build_header(final_filename)

    return response


def cross_config():
    """
    Config cross domain.
    :return:
    """
    options = dict(origins='*',
                   methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'],
                   allow_headers=['Content-Type'])

    return options
