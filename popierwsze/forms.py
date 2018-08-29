from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from popierwsze.models import User


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
# pole tekstowe "Username" --> DataRequired - oznacza, że pole nie może być puste, Length określa dopuszczalną długość

    email = StringField("Email", validators=[DataRequired(), Email()])
                    # pole nie może być puste oraz --> Email sprawdza/waliduje poprawnośc zapisanego adresu email

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
                                                    #walidator EqualTo sprawdza, czy pole takie samo jak password
    submit = SubmitField("Sing up")

    def validate_username(self, username):      #funkcje, które wywołają się same, gdzy będziemy tworzyć klasę 'registerform'
        user = User.query.filter_by(username=username.data).first() #jeśli w bazie bedzie takia nazwa, to zwróci pierwszą, jeśli nie to zwróci non
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first() #jeśli w bazie bedzie takia nazwa, to zwróci pierwszą, jeśli nie to zwróci non
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    #zapamiętaj, że sie zalogowałem, pole boolean (true/fals

    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
# pole tekstowe "Username" --> DataRequired - oznacza, że pole nie może być puste, Length określa dopuszczalną długość

    email = StringField("Email", validators=[DataRequired(), Email()])
                    # pole nie może być puste oraz --> Email sprawdza/waliduje poprawnośc zapisanego adresu email
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])]) #pole obrazka, dozwolene jpg i png
    submit = SubmitField("Update")

    def validate_username(self, username):      #funkcje, które wywołają się same, gdzy będziemy tworzyć klasę 'registerform'
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() #jeśli w bazie bedzie takia nazwa, to zwróci pierwszą, jeśli nie to zwróci non
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first() #jeśli w bazie bedzie takia nazwa, to zwróci pierwszą, jeśli nie to zwróci non
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')