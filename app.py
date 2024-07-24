from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flask:flask@db:3306/flask'
app.secret_key = 'your_secret_key_here'
MAX_CONTENT_LENGHT = 1024*1024
db = SQLAlchemy(app)

migrate = Migrate(app, db)

manager = LoginManager(app)

with  app.app_context():
    migrate.init_app(app, db)
    from routes.main import *
    from routes.employees import *
    from routes.departments import *
    from routes.login import *
    from routes.user import *
    from routes.title import *
    from routes.order import *
    from models import Employees, Departaments, User, Title, OrderTitle
    db.create_all()
    #db.drop_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)