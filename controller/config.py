
class config:
    SECRET_KEY = "your_super_secret_key"  # Required for flash messages
    SQLALCHEMY_DATABASE_URI = 'sqlite:///quiz_db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Optional but recommended