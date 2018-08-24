from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm


#pliki konfiguracyjne

app = Flask(__name__)
app.config["SECRET_KEY"] = "9fa4a357a8e67403dc5631d1806f9029"
    #konsola python --> import secrets --> secrets.token_hex(16) > to daje losowy ciąg 16 znaków potrzebny do bezpieczeństwa
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///site.db' #adres /// oznacza, ze w db będzie w tym samym miejscu, co reszta plików
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)  #backref - dodaje kolumnę do modułu Post - nazwaną "author"

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




posts = [
    {
        "autor": "ina",
        "title": "post 1",
        "content": "first post content",
        "date": "21.08.2018"
    },
    {
        "autor": "tomoe",
        "title": "post 2",
        "content": "second post content",
        "date": "22.08.2018"
    }

]

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", posts=posts)
    #zwróć wygenerowaną stronę -->home, przekaż posty


@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm()       #z zakładki forms.py
    if form.validate_on_submit():       #jeśli ktoś naciśnie klawisz SUBMIT
        flash(f"Account created for {form.username.data}!", "success")  #wyświetl wiadomość flasz(wiadomosć, categoria)
        return redirect(url_for("home"))        #przekieruj na stronę startową
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    form = LoginForm()       #z zakładki forms.py
    if form.validate_on_submit():   #tu trochę inny kod niż Corey
        flash("You have been logged in!", "success")
        return redirect(url_for("home"))
    return render_template("login.html", title="Login", form=form)

if __name__ == "__main__":
    app.run(debug=True)
