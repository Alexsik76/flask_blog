from flask import render_template
from flask_login import user_logged_in, user_logged_out
from app import turbo


def live_log_in_info(app):
    @user_logged_in.connect_via(app)
    def log_in_info(sender, user):
        print('logged in')
        turbo.push(turbo.update(render_template('auth/_user_logged_in.html', user=user), 'user-actions-info'))

    @user_logged_out.connect_via(app)
    def log_out_info(sender, user):
        print('logged out')
        turbo.push(turbo.update(render_template('auth/_user_logged_out.html', user=user), 'user-actions-info'))
