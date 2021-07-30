from flask import render_template, request, appcontext_tearing_down
from flask_login import user_logged_in, user_logged_out, current_user
from app import turbo, socketio


def live_log_in_info(app):
    target = 'user-actions-info'

    @user_logged_in.connect_via(app)
    def log_in_info(sender, user):
        turbo.push(turbo.update(render_template('auth/_user_logged_in.html', user=user.first_name), target=target))

    @user_logged_out.connect_via(app)
    def log_out_info(sender, user):
        turbo.push(turbo.update(render_template('auth/_user_logged_out.html', user=user.first_name), target=target))

    # @appcontext_tearing_down.connect_via(app)
    # def context_info(sender, exc):
    #     print('Context!!!')

    @socketio.on('disconnect')
    def test_disconnect():
        if current_user.is_authenticated:
            print(f'{current_user.first_name} disconnected')
