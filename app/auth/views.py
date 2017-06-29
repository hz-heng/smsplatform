# -*- coding: utf-8 -*-

from flask import render_template, redirect, request, url_for, flash, current_app, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Identity, identity_changed, AnonymousIdentity
from .forms import LoginForm
from app.models import User
from . import auth
from app import db

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.role))
            return redirect(request.args.get('next') or url_for('index'))
        flash('用户名或密码错误', 'warning')
    return render_template("auth/login.html",
        title = "login",
        form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('auth.login'))

@auth.route('/change_password', methods=['POST'])
@login_required
def change_password():
    old_password = request.form.get('old_password')
    new_password = request.form.get('new_password')
    if current_user.verify_password(old_password):
        current_user.password = current_user.set_password(new_password)
        db.session.add(current_user)
        status = 1
        flash('密码修改成功', 'info')
    else:
        status = 0
    return jsonify(status = status)
