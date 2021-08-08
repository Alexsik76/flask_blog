import os
from functools import wraps
from flask import flash, redirect, render_template, url_for, current_app, Markup, request
from flask_login import login_user, login_required, logout_user, current_user
from app.auth import bp
from app.auth.forms import SignUpForm, RegistrationForm, LoginForm, ResetPasswordForm, NewPasswordForm, UserForm
from app.auth.email import send_email
from itsdangerous import URLSafeTimedSerializer
from app.models import User
from app import db


def offer_to_log_in(email: str):
    href = f"""<a href="{url_for('auth.login', email=email)}" class="danger-link">Log In</a>"""
    message = f"The email: {email} is used. Please {href}."
    flash(Markup(message), 'danger')


def get_email_from_token(token):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    return email


def redirect_authenticated(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and current_user.email == get_email_from_token(kwargs.get('token')):
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/signup', methods=['GET', 'POST'])
async def signup():
    form = SignUpForm()
    is_busy = bool(User.query.filter_by(email=form.email.data).first())
    if form.validate_on_submit() and not is_busy:
        await send_email(form.email.data, goal='registration')
        flash('To continue registration, follow the link in the letter.', 'info')
        return redirect(url_for('main.index'))
    elif is_busy:
        offer_to_log_in(form.email.data)
    return render_template('auth/signup.html', form=form)


@bp.route('/register/<token>', methods=['GET', 'POST'])
@redirect_authenticated
def register(token):
    form = RegistrationForm()
    email = get_email_from_token(token)
    if bool(User.query.filter_by(email=email).first()):
        offer_to_log_in(email)
        return redirect(url_for('main.index'))
    form.email.data = email
    if form.validate_on_submit():
        new_user = User(
            email=email,
            first_name=form.first_name.data,
            last_name=form.last_name.data
        )
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        if not os.path.isdir(os.path.join(current_app.config['UPLOAD_PATH'], str(new_user.id))):
            os.mkdir(os.path.join(current_app.config['UPLOAD_PATH'], str(new_user.id)))
        flash('You can log in', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if email := request.args.get('email'):
        form.email.data = email
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user:
            flash(f'User with email {form.email.data} not registered', 'danger')
            return redirect(url_for('auth.signup'))
        elif not user.check_password(form.password.data):
            flash('Wrong password', 'danger')
            return redirect(url_for('main.index'))
        else:
            login_user(user, remember=form.remember_me.data)
            flash('Successful login', 'success')
            return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)


@bp.route('/log_out', methods=['GET', 'POST'])
@login_required
def log_out():
    logout_user()
    flash('You are logged out', 'info')
    return redirect(url_for('main.index'))


@bp.route('/reset_password', methods=['GET', 'POST'])
async def reset_password():
    form = ResetPasswordForm()
    if current_user.is_authenticated:
        form.email.data = current_user.email
        form.email.render_kw = {'disabled': True}
    is_present = bool(User.query.filter_by(email=form.email.data).first())
    if form.validate_on_submit():
        if is_present:
            await send_email(form.email.data, goal='reset')
            flash('To continue reset password, follow the link in the letter.', 'info')
            return redirect(url_for('main.index'))
        else:
            href = f"""<a href="{url_for('auth.signup', email=form.email.data)}" class="danger-link">Sign up</a>"""
            message = f"The email: {form.email.data} not founded. Please {href} or use correct email."
            flash(Markup(message), 'danger')
    return render_template('auth/signup.html', form=form)


@bp.route('/new_password/<token>', methods=['GET', 'POST'])
def new_password(token):
    form = NewPasswordForm()
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'])
    form.email.data = email
    user = User.query.filter_by(email=email).first()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Password was changed. You can log in', 'success')
        return redirect(url_for('main.index'))
    elif form.is_submitted():
        return render_template('auth/new_password.html', form=form), 422
    return render_template('auth/new_password.html', form=form)


@bp.route('/user_page', methods=['GET', 'POST'])
@login_required
def user_page():
    form = UserForm(obj=current_user)
    if form.validate_on_submit():
        is_changed = False
        for field in 'email', 'first_name', 'last_name':
            if getattr(form, field).data is not getattr(current_user, field):
                setattr(current_user, field, getattr(form, field).data)
                is_changed = True
        if is_changed:
            db.session.commit()
    return render_template('auth/user_page.html', form=form)
