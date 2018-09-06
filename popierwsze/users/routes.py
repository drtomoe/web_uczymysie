from flask import render_template, url_for, flash, redirect, request, Blueprint
from popierwsze import db, bcrypt
from popierwsze.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from popierwsze.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from popierwsze.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # jeśli użytkownik jest już zalogowany/ funkcja z importu
        return redirect(url_for('main.home'))
    form = RegistrationForm()  # z zakładki forms.py
    if form.validate_on_submit():  # jeśli ktoś naciśnie klawisz SUBMIT/zatwierdz
        hashed_pas = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # zakodować hasło
        user = User(username=form.username.data, email=form.email.data,
                    password=hashed_pas)  # przekazać dane z formularza, ale hasło dać zakodowane
        db.session.add(user)  # dodać do bazy danych i zakomitować
        db.session.commit()
        flash("Your account has been created! You are now able to log in.",
              "success")  # wyświetl wiadomość flasz(wiadomosć, categoria)
        return redirect(url_for("users.login"))  # przekieruj na stronę startową
    return render_template("register.html", title="Register", form=form)


@users.route("/login", methods=['GET', 'POST'])  # get, post  = funcje http
def login():
    if current_user.is_authenticated:  # jeśli użytkownik jest już zalogowany/ funkcja z importu
        return redirect(url_for('main.home'))

    form = LoginForm()  # z zakładki forms.py
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # jeśli taki email istnieje w db, zwróci pierwszego, inaczej non
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)  # funkcja z importu
            next_page = request.args.get('next')        #pobierze, jeśli istnieje, z wiersza adresu stronę, z której naj przekierowało do logowania, np 'account'
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  #dziwna składnia, turnery condition, ale działa
        else:
            flash("Login unsuccessful. Please check email and password", "danger")

    return render_template("login.html", title="Login", form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required  # z importu
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:       #jeśli mamy obrazek
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file  #wstawiamy w db przesłany plik (ze zmienioną nazwą)

        current_user.username=form.username.data        #podmieniamy w db username i emaila
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username      #wstawi w pola dane domyślne dla obecnego użytkownika
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # 'static' jako stały adres, plik z katalogu 'profile_pics' i plik o nazwie takiej jak w db / domyślnie default
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()       #pobierz usera
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:  # jeśli użytkownik jest już zalogowany/ funkcja z importu
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been send with instruction to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template("reset_request.html", title='Reset Password', form=form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])  #parametry w linkach podawane są w nawiasach < >
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:        #weryfikacja wróci pusta, jeśli token nie będzie się zgadzał, inaczej 'if user is None'
        flash('This is an invalid or expired token', 'warning')     #'warning' jest żłótym flashem
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():  # jeśli ktoś naciśnie klawisz SUBMIT/zatwierdz
        hashed_pas = bcrypt.generate_password_hash(form.password.data).decode('utf-8')  # zakodować hasło
        user.password = hashed_pas
        db.session.commit()
        flash("Your password has been updated! You are now able to log in.",
              "success")  # wyświetl wiadomość flasz(wiadomosć, categoria)
        return redirect(url_for("users.login"))  # przekieruj na stronę startową
    return render_template('reset_token.html', title='Reset Password', form=form)
