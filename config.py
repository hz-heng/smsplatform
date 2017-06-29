# -*- coding: utf-8 -*-

import os

#版本号设置
VERSION = 'Ver: 1.0.2'

#csrf设置
CSRF_ENABLED = True
SECRET_KEY = 'abxdefghuijk'

#数据库设置
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'sms.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

#阿里大于api设置
URL = "http://gw.api.taobao.com/router/rest"
APPKEY = "" #填入自己的APPKEY
SECRET = "" #填入自己的SECRET

