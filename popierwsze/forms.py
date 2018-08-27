from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
# pole tekstowe "Username" --> DataRequired - oznacza, że pole nie może być puste, Length określa dopuszczalną długość

    email = StringField("Email", validators=[DataRequired(), Email()])
                    # pole nie może być puste oraz --> Email sprawdza/waliduje poprawnośc zapisanego adresu email

    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
                                                    #walidator EqualTo sprawdza, czy pole takie samo jak password
    submit = SubmitField("Sing up")


class LoginForm(FlaskForm):

    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember me")
    #zapamiętaj, że sie zalogowałem, pole boolean (true/fals

    submit = SubmitField("Login")