import os
from werkzeug.utils import secure_filename
from flask import render_template, flash, redirect, url_for, current_app, send_from_directory, Response
from app import db
from app.main import bp
from app.main.forms import CreatePostForm
from werkzeug.exceptions import NotFound
from flask_login import login_required, current_user, logout_user
from app.models import User, Post
from config import get_path_safe


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    posts = Post.query.filter(Post.user_id.is_not(None)).all() # noqa
    return render_template('index.html', title='Home', posts=posts)


@bp.route('/admin')
@login_required
def admin():
    if current_user.is_admin:
        users = User.query.all()
        posts = Post.query.all()
    else:
        users = []
        posts = Post.query.filter_by(user_id=current_user.id).all()
    return render_template('admin_page.html', users=users, posts=posts)


@bp.route('/_delete_user/<user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if current_user.is_admin:
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return 'Success', 200
    else:
        flash('Operation is not permitted.', 'danger')
        return redirect(url_for('main.index'))


@bp.route('/_delete_post/<post_id>', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user.is_admin or current_user is post.author:
        db.session.delete(post)
        db.session.commit()
        return 'Success', 200
    else:
        flash('Operation is not permitted.', 'danger')
        return redirect(url_for('main.index'))


@bp.route('/_close_window_info')
def logout_closed():
    if current_user.is_authenticated:
        logout_user()
    return Response(status=200, mimetype='application/json')


@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        img = form.img.data
        filename = secure_filename(img.filename)
        img.save(os.path.join
                 (get_path_safe(current_app.config['UPLOAD_PATH'], current_user.get_id()),
                  filename))
        new_post = Post(
            title=form.title.data,
            body=form.body.data,
            img=filename,
            user_id=current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        flash('You are created new post.', 'info')
        return redirect(url_for('main.index'))
    return render_template('create_post.html', form=form)


@bp.route('/uploads/<author_id>/<filename>')
@login_required
def upload(author_id=None, filename=None):
    try:
        img = send_from_directory(os.path.join(
            current_app.config['UPLOAD_PATH'], author_id), filename)
    except NotFound:
        img = send_from_directory(os.path.join(current_app.config['BASE_DIR'],
                                               current_app.config['STATIC_FOLDER']),
                                  'not-found.png')
    return img
