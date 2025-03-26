from flask import Flask, render_template
from controller.database import db
from werkzeug.security import generate_password_hash
from sqlalchemy import event

import enum

app = Flask(__name__,template_folder='html_temps')


from controller.model import *
from controller.model import QualificationEnum
#for value in QualificationEnum:
    #print(value.name, "->", value.value)

def enable_foreign_keys():
    @event.listens_for(db.engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

with app.app_context():
    from controller.config import config
    app.config.from_object(config)
    
    db.init_app(app)
    enable_foreign_keys()
    db.create_all()
    
    admin_role = Role.query.filter_by(name = 'admin').first()
    if not admin_role:
        admin_role = Role(
            name = 'admin',
            description = 'admin role'
        )
        db.session.add(admin_role) 

    user_role = Role.query.filter_by(name = 'user').first()
    if not user_role:
        customer_role = Role(
            name = 'user',
            description = 'user role'
        )
        db.session.add(customer_role)

    admin = User.query.filter_by(email = 'admin@gmail.com').first()
    if not admin:
        admin = User(
            name = 'admin',
            email = 'admin@gmail.com',
            password= generate_password_hash('2003'),
            #class_=QualificationEnum("Class 8"),
            roles = [admin_role]
            
        )

        db.session.add(admin)
        
    db.session.commit()


from controller.routes import *
if __name__ == '__main__':
 app.run(port=8080, debug=True)