# -*- coding: utf-8 -*-

from flask_principal import Principal, Permission, RoleNeed

principal = Principal()

admin_permission = Permission(RoleNeed('admin'))

