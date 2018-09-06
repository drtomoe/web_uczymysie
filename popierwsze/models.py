from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from popierwsze import db, login_menager
from flask_login import UserMixin


        ##klasy-tabele które będą zapisywane w bazie danych db

@login_menager.user_loader      #funkcja dekoracyjna do utrzymywania logowania użytkownika
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):    #userMixin pozwoli nam dziedziczyć funkcje tej klasy/logowanie
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)  #backref - dodaje kolumnę do modułu Post - nazwaną "author"

    #metoda do robienia tokenu bezpieczeństwa do zmieniania hasła/maila

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')        #generujemy/zwracamy token przypisany dla tego konkretnego użytkownika/id

    @staticmethod       #dekorator, który mówi, że metoda nie zmienia nic w klasie
    def verify_reset_token(token):      #nie zmiania nic w User, wiec nie trzeba zmiennej 'self'
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']       #czy user_id równa się 'user_id' tego tokena/biblioteki
        except:
            return None     #nic nie zwracaj
        return User.query.get(user_id)      #zwróci Usera o podanym id, jeśli 'try' przejdzie


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #user.id z małej bo to odniesienie do wiersza tabeli User a nie do całej klasy

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

