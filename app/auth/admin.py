from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from flask import redirect, request, url_for, flash
from flask_admin import AdminIndexView, expose
from app.models import User


class AppUserModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and getattr(current_user, 'email', None) == 'alex@jurist.vn.ua'

    def inaccessible_callback(self, name, **kwargs):
        flash("You can't access this page", 'danger')
        return redirect(url_for('main.index', next=request.url))


class AppPostModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        flash("You can't access this page", 'warning')
        return redirect(url_for('auth.login', next=request.url))


class MyHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        number_of_users = None
        if current_user.is_authenticated:
            number_of_users = User.query.count()
        return self.render('admin/index.html', number_of_users=number_of_users)
