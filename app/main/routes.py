from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app.main import bp
from app.main.forms import CreatePostForm
from flask_login import login_required


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@bp.route('/new_post')
@login_required
def create_post():
    form = CreatePostForm()
    return render_template('create_post.html', form=form)
