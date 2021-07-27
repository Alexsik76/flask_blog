from flask import render_template
from flask_login import user_logged_in, user_logged_out
from app import turbo


def live_log_in_info(app):
    target = 'user-actions-info'

    @user_logged_in.connect_via(app)
    def log_in_info(sender, user):
        turbo.push(turbo.append(render_template('auth/_user_logged_in.html', user=user), target=target))
        app.logger.info('Func log_in_info started.')

    @user_logged_out.connect_via(app)
    def log_out_info(sender, user):
        turbo.push(turbo.append(render_template('auth/_user_logged_out.html', user=user), target=target))
        app.logger.info('Func log_out_info started.')
