from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
db_filename = "database.db"


def create_app():
    app = Flask(__name__,static_url_path='/static')
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_filename}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User

    create_database(app)

    login_manager = LoginManager() #Allows access to pages if logged in, Holds credentials, ...etc
    login_manager.login_view = "auth.login" #Redirects user to login page if not loggedin.
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #Allows admin to access information about user from database. Will be important for backend.
    return app

def create_database(app):
    if not path.exists("code/" + db_filename):
        db.create_all(app=app)
        print("DATABASE CREATED!!!!!!!!!!!!!!!")

