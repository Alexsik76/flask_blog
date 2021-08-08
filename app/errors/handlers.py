from flask import render_template
from app import db
from app.errors import bp
from werkzeug.exceptions import RequestEntityTooLarge


@bp.app_errorhandler(404)
def not_found_error(e):
    return render_template('errors/404.html', title=e), 404


@bp.app_errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('errors/500.html',  title=e), 500


@bp.app_errorhandler(RequestEntityTooLarge)
def file_too_large(e):
    return render_template('errors/413.html', title=e), 413
