from flask import Flask, render_template, url_for

app = Flask(__name__)

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

def hello():
    return render_template("home.html", posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


if __name__ == "__main__":
    app.run(debug=True)
