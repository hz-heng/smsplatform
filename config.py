import os

#the version
VERSION = 'Ver: 1.0.2'

#csrf settings
CSRF_ENABLED = True
SECRET_KEY = 'abxdefghuijk'

#database settings
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'sms.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

#alidayu settings
URL = "http://gw.api.taobao.com/router/rest"
APPKEY = ""
SECRET = ""

