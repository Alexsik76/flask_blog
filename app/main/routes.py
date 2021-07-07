from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app.main import bp
from app.main.forms import CreatePostForm
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.models import Post


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@bp.route('/new_post')
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        img = form.img.data
        filename = secure_filename(img.filename)
        new_post = Post(
            title=form.title.data,
            body=form.body.data,
            img=filename,
            user_id=current_user.id
        )

    return render_template('create_post.html', form=form)
