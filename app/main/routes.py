import imghdr
import os
from flask import render_template, flash, redirect, url_for, current_app, send_from_directory, Response
from app import db
from app.main import bp
from app.main.forms import CreatePostForm
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound
from flask_login import login_required, current_user
from app.models import Post
from config import get_path_safe


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)


def validate_image(stream):
    header = stream.read(512)
    stream.seek(0)
    file_format = imghdr.what(None, header)
    if not file_format:
        return None
    return '.' + (file_format if file_format != 'jpeg' else 'jpg')


@bp.route('/_user_info')
def user_info():
    user = current_user.first_name if current_user.is_authenticated else current_user
    #turbo.push(turbo.update(render_template('auth/_user_logged_out.html', user=user), target='user-actions-info'))
    return Response(status=200)


@bp.route('/new_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        img = form.img.data
        filename = secure_filename(img.filename)
        file_ext = os.path.splitext(filename)[1].lower()
        from_stream_ext = validate_image(img.stream)
        if file_ext != from_stream_ext:
            flash('Files content is not valid!', 'danger')
            return render_template('create_post.html', form=form)
        img.save(os.path.join(get_path_safe(current_app.config['UPLOAD_PATH'], current_user.get_id()), filename))
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
def upload(author_id, filename):
    try:
        img = send_from_directory(os.path.join(
            current_app.config['UPLOAD_PATH'], author_id), filename)
    except NotFound:
        img = send_from_directory(os.path.join(current_app.config['BASE_DIR'],
                                               current_app.config['STATIC_FOLDER']),
                                  'not-found.png')
    return img
