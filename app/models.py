# -*- coding: utf-8 -*-

from flask_login import UserMixin
from app import db
import bcrypt
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func

users_templates = db.Table('users_templates',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('template_id', db.Integer, db.ForeignKey('templates.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255), nullable=False) #权限admin或user
    templates = db.relationship('Template', secondary=users_templates, backref=db.backref('users'))
    records = db.relationship('Record', backref=db.backref('users'))

    def __init__(self, username, password, role):
        self.username = username
        self.password = self.set_password(password)
        self.role = role

    def set_password(self, password):
        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))
    
    def change_password(self, password):
        self.password = self.set_password(password)

class Template(db.Model):
    __tablename__ = 'templates'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    type = db.Column(db.String(255), nullable=False)
    sign = db.Column(db.String(255),nullable=False)
    param = db.Column(db.Boolean, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __init__(self, code, name, type, sign, param, content):
        self.code = code
        self.name = name
        self.type = type
        self.sign = sign
        self.param = param
        self.content = content

class Record(db.Model):
    __tablename__ = 'records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    number = db.Column(db.String(16), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(255), nullable=False)
    sendtime = db.Column(TIMESTAMP, server_default=func.now())

    def __init__(self, number, name, content, status):
        self.number = number
        self.name = name
        self.content = content
        self.status = status
