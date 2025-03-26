from controller.database import db

class User(db.Model):
    # Although I can Creating the Class name = 'User' the table name will be 'user'
    #if my Class name = 'UserTable' the table name will be 'user_table'
    #If am not okay with that I can create tables with custom names to using the following attribute:
    #__tablename__ = "user_table_new"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable = False)
    roles = db.relationship('Role', secondary='user_role')

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)

class UserRole(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id'),nullable= False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'),nullable= False)
