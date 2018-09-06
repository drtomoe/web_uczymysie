import os
import secrets
from PIL import Image       #modół Pillow do obróbki obrazków
from flask import url_for, current_app
from popierwsze import mail          #z __init__
from flask_mail import Message


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)       #zmienimy nazwę wgrywanego obrazka, żeby nie wgrało się coś niedobrego do db
    _, f_ext = os.path.splitext(form_picture.filename) #dzieli nazwę na nazwę i rozszerzenie, będziemy potrzebować tego drugiego
        # sam '_' oznacza zmienną, której nigdzie nie będziemy używać - tu jest to nazwa pliku
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)    #przeformatowanie do założonych wymiarów
    i.save(picture_path)

    return picture_fn       #zwraca nową nazwę obrazka


# funkcja nie-ścieżka, potrzebna do ścieżki poniżej
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password reset request', sender='noreply@demo.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}           

If you did not make this request then simply ignore this email and no changes will be made.
'''  # _external = buduje pełen adres url, a nie tylko końcówkę
    # przy multi-stringu -3x'- trzeba pisać tekst od samego początku wiersza bez tabulatorów ,
    mail.send(msg)