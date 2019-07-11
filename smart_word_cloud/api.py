# -*- coding:utf-8 -*-
import os

from flask import request, jsonify
from werkzeug.utils import secure_filename
from .app import app
from .clouds import SmartWordCloud
from .utils import to_response


def allowed_file(filename):
    allowed_extensions = tuple(['txt'])

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


@app.route('/api/clouds', methods=['POST'])
def get_clouds():
    """
    获取词云图片和词频统计文件
    :return:
    """
    if 'file' not in request.files:
        return jsonify('Can not get file.'), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify('The filename is empty'), 400

    if f and allowed_file(f.filename):
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_DIR'], filename)
        f.save(file_path)  # 保存上传的文件

        rendered_file = SmartWordCloud(file_path).save()

        return to_response(rendered_file , filename)

    return jsonify('Not support to render the file.'), 400
