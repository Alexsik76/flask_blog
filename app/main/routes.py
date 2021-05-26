from flask import render_template, flash, redirect, url_for, request, g, jsonify, current_app
from app.main import bp
from flask_login import current_user, login_user


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')
