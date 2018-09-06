from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from popierwsze.config import Config

#pliki konfiguracyjne, inicjalizujemy aplikacje app, db, szyfrowanie, logowanie/sesję
#dzięki __init__.py program wie, że dany folder to 'paczka' programowa

db = SQLAlchemy()
bcrypt = Bcrypt()
login_menager = LoginManager()
login_menager.login_view = 'users.login'      #jeśli chcesz wejść gdzieś, gdzie login_required, a nie jestes log_in, przekieruje cię do 'login'
login_menager.login_message_category = 'info'   #albo 'danger', albo 'succes'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)  # całe ustawienia konfiguracji z config.py

    db.init_app(app)
    bcrypt.init_app(app)
    login_menager.init_app(app)
    mail.init_app(app)

    from popierwsze.users.routes import users
    from popierwsze.posts.routes import posts
    from popierwsze.main.routes import main
    from popierwsze.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app

