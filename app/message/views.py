# -*- coding: utf-8 -*-

from flask import render_template, url_for, request, jsonify, current_app, flash
from flask_login import login_required, current_user
from . import message
from app.models import User, Template, Record
from app import db
from app.ext.alidayu import AlibabaAliqinFcSmsNumSendRequest

@message.route('/send')
@login_required
def send():
    templates = Template.query.filter(Template.users.any(id=current_user.id)).all()
    return render_template("message/send.html",
        title = "信息发送",
        icon = "send icon",
        templates = templates)

@message.route('/gettemplate', methods=['POST'])
def gettemplate():
    id = request.get_data()
    template = Template.query.filter_by(id=id).first()
    return jsonify(name = template.name,
        code = template.code,
        type = template.type,
        sign = template.sign,
        param = template.param,
        content = template.content)

@message.route('/sendmsg', methods=['POST'])
def sendmsg():
    config = current_app.config
    url = config.get('URL')
    appkey = config.get('APPKEY')
    secret = config.get('SECRET')

    req = AlibabaAliqinFcSmsNumSendRequest(appkey, secret, url)

    phone = request.form.get("phone")
    code = request.form.get("code")
    sign = request.form.get("sign")
    date = request.form.get("date")
    content = request.form.get("content")
    name = request.form.get("name")
    
    req.extend = str(current_user.id)
    req.sms_type = "normal"
    req.sms_free_sign_name = sign
    req.rec_num = str(phone)
    req.sms_template_code = code
    req.sms_param = "{\"name\":\"\", \"date\":%s}" % date
    try:
        resp = req.getResponse()
    except Exception as e:
        status_msg = "网络异常"
       #status_msg = e
    else:
        if ('error_response' in resp.keys()):
            if('sub_msg' in resp['error_response'].keys()):
                status_msg = resp['error_response']['sub_msg']
            else:
                status_msg = resp['error_response']['msg']
        elif (resp['alibaba_aliqin_fc_sms_num_send_response']['result']['success']):
            flash("发送成功", "info")
            status_msg = "发送成功"
        else:
            status_msg = "发送失败"
   
    #添加发送记录
    if (date):
        send_content = content.replace('${date}', date)
    else:
        send_content = content
    current_user.records.append(Record(number=phone, name=name, content=send_content, status=status_msg))
    db.session.add(current_user)
     
    return jsonify(status=status_msg)

@message.route('/record')
#@login_required
def record():
    if (current_user.role == "admin"):
        records = Record.query.filter().all()
    else:
        records = Record.query.filter_by(user_id=current_user.id).all()
    return render_template("message/record.html",
        icon = "browser icon",
        title = "发送记录",
        records = records)
