from flask import render_template, redirect, request, jsonify, flash,url_for
from flask_login import login_required
from app.ext.principal import admin_permission
from app.models import User, Template
from app import db

from . import admin

@admin.route('/user')
@login_required
@admin_permission.require()
def user():
    users = User.query.filter_by(role="user").all()
    templates = Template.query.all()
    return render_template("admin/user.html",
        icon="users icon",
        title="用户管理",
        users=users,
        templates=templates)

@admin.route('/adduser', methods=['POST'])
@login_required
@admin_permission.require()
def adduser():
    username = request.form.get("username")
    password = request.form.get("password")
    if (User.query.filter_by(username=username).first()):
        status_msg = "用户已存在"
    else:
        try:
            user = User(username=username, password=password, role='user')
            db.session.add(user)
            flash("成功添加新用户", 'info')
            status_msg = 'ok'
        except:
            status_msg = "添加用户失败"
    return jsonify(status=status_msg)

@admin.route('/removeuser', methods=['POST'])
@login_required
@admin_permission.require()
def removeuser():
    user_id = request.get_data()
    try:
        user = User.query.filter_by(id=user_id).first()
        db.session.delete(user)
        flash("成功删除用户", 'info')
        status_msg = 'ok'
    except:
        status_msg = "删除用户失败"
    return jsonify(status=status_msg)

@admin.route('/usertemplates', methods=['POST'])
@login_required
@admin_permission.require()
def usertemplates():
    user_id = request.get_data()
    user = User.query.filter_by(id=user_id).first()
    templates = Template.query.filter(Template.users.any(id=user_id)).all()
    list = [template.id for template in templates]
    return jsonify(tempids=list,username=user.username)

@admin.route('/authedit', methods=['POST'])
@login_required
@admin_permission.require()
def authedit():
    user_id = request.form.get("userid")
    temps = request.form.getlist("tempids")#获取选择的模板列表

    user = User.query.filter_by(id=user_id).one()
    templates = Template.query.filter(Template.users.any(id=user_id)).all()
    #清空用户的模板列表
    user.templates.clear()
    #添加授权模板
    if len(temps):
        for temp_id in temps:
            template = Template.query.filter_by(id=temp_id).one()
            user.templates.append(template)
    status_msg = 'ok'
    return jsonify(status=status_msg)

@admin.route('/addtemp', methods=['POST'])
@login_required
@admin_permission.require()
def addtemp():
    name = request.form.get("name")
    code = request.form.get("code")
    type = request.form.get("type")
    sign = request.form.get("sign")
    param = request.form.get("param")
    content = request.form.get("content")

    if(Template.query.filter_by(code=code).first()):
        status_msg = "模板已存在"
    else:
        try:
            #添加模板时直接授权给admin
            admin = User.query.filter_by(role="admin").one()
            admin.templates.append(Template(name=name, code=code, type=type, sign=sign, param=param=='1', content=content))
            db.session.add(admin)
            flash("成功添加模板", 'info')
            status_msg = 'ok'
        except:
            status_msg = "添加模板失败"   

    return jsonify(status=status_msg)

@admin.route('/removetemp', methods=['POST'])
@login_required
@admin_permission.require()
def removetemp():
    temp_id = request.get_data()
    try:
        template = Template.query.filter_by(id=temp_id).first()
        db.session.delete(template)
        flash("成功删除模板", 'info')
        status_msg = 'ok'
    except:
        status_msg = "删除模板失败"
    return jsonify(status=status_msg)

@admin.route('/gettemp', methods=['POST'])
@login_required
@admin_permission.require()
def gettemp():
    temp_id = request.get_data()
    temp = Template.query.filter_by(id=temp_id).first()
    return jsonify(name = temp.name,
                   code = temp.code,
                   type = temp.type,
                   sign = temp.sign,
                   param = '1' if temp.param else '0',
                   content = temp.content)

@admin.route('/edittemp', methods=['POST'])
@login_required
@admin_permission.require()
def edittemp():
    id = request.form.get("id")
    name = request.form.get("name")
    code = request.form.get("code")
    type = request.form.get("type")
    sign = request.form.get("sign")
    param = request.form.get("param")
    content = request.form.get("content")
    try:
        temp = Template.query.filter_by(id=id).first()
        temp.name = name 
        temp.code = code
        temp.type = type
        temp.sign = sign
        temp.param = param == '1' #转为boolen类型
        temp.content = content
        db.session.commit()
        flash("成功更新模板", 'info')
        status_msg = "ok"
    except:
        status_msg = "更新模板失败"
    return jsonify(status=status_msg)

@admin.route('/template')
@login_required
@admin_permission.require()
def template():
    templates = Template.query.all()
    return render_template("admin/template.html",
        icon="mail outline icon",
        title="信息模板",
        templates=templates)
