from flask import render_template, url_for, flash, redirect, request
from popierwsze import app, db, bcrypt
from popierwsze.forms import RegistrationForm, LoginForm
from popierwsze.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

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
    # zwróć wygenerowaną stronę -->home, przekaż posty


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # jeśli użytkownik jest już zalogowany/ funkcja z importu
        return redirect(url_for('home'))
    form = RegistrationForm()  # z zakładki forms.py
    if form.validate_on_submit():  # jeśli ktoś naciśnie klawisz SUBMIT/zatwierdz
        hashed_pas = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # zakodować hasło
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_pas)  # przekazać dane z formularza, ale hasło dać zakodowane
        db.session.add(user)  # dodać do bazy danych i zakomitować
        db.session.commit()
        flash("Your account has been created! You are now able to log in.",
              "success")  # wyświetl wiadomość flasz(wiadomosć, categoria)
        return redirect(url_for("login"))  # przekieruj na stronę startową
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])  # get, post  = funcje http
def login():
    if current_user.is_authenticated:  # jeśli użytkownik jest już zalogowany/ funkcja z importu
        return redirect(url_for('home'))

    form = LoginForm()  # z zakładki forms.py
    if form.validate_on_submit():  # tu trochę inny kod niż Corey
        user = User.query.filter_by(
            email=form.email.data).first()  # jeśli taki email istnieje w db, zwróci pierwszego, inaczej non
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  # funkcja z importu
            next_page = request.args.get('next')        #pobierze, jeśli istnieje, z wiersza adresu stronę, z której naj przekierowało do logowania, np 'account'
            return redirect(next_page) if next_page else redirect(url_for('home'))  #dziwna składnia, turnery condition, ale działa
        else:
            flash("Login unsuccessful. Please check email and password", "danger")

    return render_template("login.html", title="Login", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account')
@login_required  # z importu
def account():
    return render_template("account.html", title="Account")
