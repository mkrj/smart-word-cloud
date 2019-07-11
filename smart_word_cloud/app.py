# -*- coding:utf-8 -*-
import traceback
import os
import sys

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from .utils import cross_config


app = Flask(__name__)
CORS(app, **cross_config())

app.config['SAVED_DIR'] = os.getenv('SAVED_DIR')
app.config['UPLOAD_DIR'] = os.getenv('UPLOAD_DIR')
app.config['STOPWORDS_FILE'] = os.getenv('STOPWORDS_FILE')  # 停用词表文件
app.config['FONT_FILE'] = os.getenv('FONT_FILE')  # 中文字体文件
app.config['IMAGE_FILE'] = os.getenv('IMAGE_FILE')


@app.errorhandler(Exception)
def errors(e):
    message = getattr(e, 'description', None) or getattr(e, 'msg', None) or str(e)

    error = {
        'code': str(getattr(e, 'code', 500)),
        'name': str(getattr(e, 'name', '')),
        'message': message
    }

    if app.debug or os.getenv('ENV') == 'dev':
        error['trace'] = traceback.format_exception(*sys.exc_info())
        print(''.join(error['trace']))

    code = error['code'] if isinstance(e, HTTPException) else 500
    # 注：error['code'] 有可能是字符串，比如 SQL语法错误引起的 Exception
    return jsonify(error), int(code)
