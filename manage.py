from app import app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Template

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

#初始化admin账号
@manager.command
def initdata():
    db.session.add(User(username='admin', password='admin', role='admin'))
    db.session.commit()

if __name__ == "__main__":
    manager.run()
