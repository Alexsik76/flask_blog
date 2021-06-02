from flask import flash, redirect, render_template, url_for, current_app
from app.auth import bp
from app.auth.forms import SignUpForm, RegistrationForm
from app.auth.email import send_registration_email
from itsdangerous import URLSafeTimedSerializer
from app.models import User
from app import db


@bp.route('/signup', methods=['GET', 'POST'])
async def signup():
    form = SignUpForm()
    is_busy = bool(User.query.filter_by(email=form.email.data).first())
    if form.validate_on_submit() and not is_busy:
        await send_registration_email(form.email.data)
        flash('To continue registration, follow the link in the letter.', 'info')
        return redirect(url_for('main.index'))
    elif is_busy:
        flash(f'The email: {form.email.data} is used.', 'danger')

    return render_template('auth/signup.html', form=form)


@bp.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    form = RegistrationForm()
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'])
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
        flash('You can log in', 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)
