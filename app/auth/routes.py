from flask import flash, redirect, render_template, url_for
from app.auth import bp
from app.auth.forms import SignUpForm
from app.auth.email import send_registration_email


@bp.route('/signup', methods=['GET', 'POST'])
async def signup():
    form = SignUpForm()
    print(form.email.data, form.validate_on_submit())
    if form.validate_on_submit():
        await send_registration_email(form.email.data)
        flash('To continue registration, follow the link in the letter.')
        return redirect(url_for('main.index'))
    return render_template('auth/signup.html', form=form)


@bp.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    pass
