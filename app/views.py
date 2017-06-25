from flask import redirect, url_for
from flask_login import current_user
from app import app

@app.route('/')
def index():
    return redirect(url_for('message.send'))

@app.context_processor
def menu():
    menus = [
        {
            'require_type': 1,
            'id': 'send',
            'link': '/message/send',
            'name': '信息发送',
            'icon': 'send icon'
        },
        {
            'require_type': 1,
            'id': 'record',
            'link': '/message/record',
            'name': '发送记录',
            'icon': 'browser icon'
        },
        {
            'require_type': 100,
            'id': 'user',
            'link': '/admin/user',
            'name': '用户管理',
            'icon': 'users icon'
        },
        {
            'require_type': 100,
            'id': 'templates',
            'link': '/admin/template',
            'name': '信息模板',
            'icon': 'mail outline icon'
        }
    ]
    if current_user.is_authenticated:
        type = ["管理员", 100] if current_user.role == 'admin' else ["普通用户", 1]
    else:
        type = ""
    return dict(menus = menus, type=type)
