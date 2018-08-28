from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#pliki konfiguracyjne, inicjalizujemy aplikacje app, db, szyfrowanie, logowanie/sesję

app = Flask(__name__)
app.config["SECRET_KEY"] = "9fa4a357a8e67403dc5631d1806f9029"
    #konsola python --> import secrets --> secrets.token_hex(16) > to daje losowy ciąg 16 znaków potrzebny do bezpieczeństwa
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db' #adres /// oznacza, ze w db będzie w tym samym miejscu, co reszta plików
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_menager = LoginManager(app)
login_menager.login_view = 'login'      #jeśli chcesz wejść gdzieś, gdzie login_required, a nie jestes log_in, przekieruje cię do 'login'
login_menager.login_message_category = 'info'   #albo 'danger', albo 'succes'

from popierwsze import routes       #dopiero po wywołaniu app, bo inaczej wpadnie w pętlę wywoławczą/importową