import os
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

# WTF settings
CSRF_ENABLED = True
SECRET_KEY = 'boom-shake-shake-shake-the-room'
