from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.ext.login import login_manager
from app.ext.principal import principal
from flask_login import current_user
from flask_principal import identity_loaded, RoleNeed, UserNeed

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

#模板注册
from app.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from app.message import message as message_blueprint
app.register_blueprint(message_blueprint, url_prefix='/message')

from app.admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

#flask-login配置
login_manager.init_app(app)

#flask-principal配置
principal.init_app(app)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))

from app import views, models
