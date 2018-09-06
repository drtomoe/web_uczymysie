from flask import render_template, request, Blueprint
from popierwsze.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)    #ilość stron, domyślnie pierwsza i podane w integerach
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)        #wyciąganie postów z db - paginate będzie ściągać z podziałem na strony
    # posty posegregowany po dacie publikacji - descending - od najnowszych, po 5 na stronie
    return render_template("home.html", posts=posts)
    # zwróć wygenerowaną stronę -->home, przekaż posty


@main.route("/about")
def about():
    return render_template("about.html", title="About")