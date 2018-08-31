import os
import secrets
from PIL import Image       #modół Pillow do obróbki obrazków
from flask import render_template, url_for, flash, redirect, request, abort
from popierwsze import app, db, bcrypt          #z __init__
from popierwsze.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from popierwsze.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

        ## ścieżki/route w wierszu poleceń i logika zachowań

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)    #ilość stron, domyślnie pierwsza i podane w integerach
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)        #wyciąganie postów z db - paginate będzie ściągać z podziałem na strony
    # posty posegregowany po dacie publikacji - descending - od najnowszych, po 5 na stronie
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
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # jeśli taki email istnieje w db, zwróci pierwszego, inaczej non
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)       #zmienimy nazwę wgrywanego obrazka, żeby nie wgrało się coś niedobrego do db
    _, f_ext = os.path.splitext(form_picture.filename) #dzieli nazwę na nazwę i rozszerzenie, będziemy potrzebować tego drugiego
        # sam '_' oznacza zmienną, której nigdzie nie będziemy używać - tu jest to nazwa pliku
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)    #przeformatowanie do założonych wymiarów
    i.save(picture_path)

    return picture_fn       #zwraca nową nazwę obrazka

@app.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username      #wstawi w pola dane domyślne dla obecnego użytkownika
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    # 'static' jako stały adres, plik z katalogu 'profile_pics' i plik o nazwie takiej jak w db / domyślnie default
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template("create_post.html", title="New Post", form=form, legend='New Post')


@app.route('/post/<int:post_id>')   #zmienna typu int - w wierszu będzie widoczny numer-id posta
def post(post_id):
    #post = Post.query.get(post_id)         --> lub:
    post = Post.query.get_or_404(post_id)       #jeśli nie ma posta o tym id wywal 404error
    return render_template('post.html', title=post.title, post=post)


@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        about(403)      #przerwij i wyświetl błąd, posta nie może zmienić jeśli nie jesteś jego autorem
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()     #jak coś już jest w db (a jest bo to modyfikujemy) to tylko commit, bez add
        flash('Your message has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id ))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend='Update Post', )


@app.route('/post/<int:post_id>/delete', methods=['POST'])      #bez GET, bo nie będziemy nic pobierać, tylko kasować/updatować
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        about(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your message has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()       #pobierz usera
    posts = Post.query.filter_by(author=user).order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template("user_posts.html", posts=posts, user=user)
