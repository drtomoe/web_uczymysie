from flask import render_template, url_for, flash, redirect, request, Blueprint, abort
from flask_login import current_user, login_required
from popierwsze import db
from popierwsze.models import Post
from popierwsze.posts.forms import PostForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template("create_post.html", title="New Post", form=form, legend='New Post')


@posts.route('/post/<int:post_id>')   #zmienna typu int - w wierszu będzie widoczny numer-id posta
def post(post_id):
    #post = Post.query.get(post_id)         --> lub:
    post = Post.query.get_or_404(post_id)       #jeśli nie ma posta o tym id wywal 404error
    return render_template('post.html', title=post.title, post=post)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)      #przerwij i wyświetl błąd, posta nie może zmienić jeśli nie jesteś jego autorem
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()     #jak coś już jest w db (a jest bo to modyfikujemy) to tylko commit, bez add
        flash('Your message has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id ))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend='Update Post', )


@posts.route('/post/<int:post_id>/delete', methods=['POST'])      #bez GET, bo nie będziemy nic pobierać, tylko kasować/updatować
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your message has been deleted!', 'success')
    return redirect(url_for('main.home'))

