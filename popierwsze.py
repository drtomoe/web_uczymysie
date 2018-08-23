from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "9fa4a357a8e67403dc5631d1806f9029"
#konsola python --> import secrets --> secrets.token_hex(16)   --> to daje losowy ciąg 16 znaków

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
