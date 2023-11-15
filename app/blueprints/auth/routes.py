from app.blueprints.auth import auth
from .forms import LoginForm, SignupForm
from flask import request, flash, redirect, url_for, render_template
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, Trainer {queried_user.first_name}!', 'success')
            return redirect(url_for('main.home'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)
    
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        user = User(first_name, last_name, email, password)

        db.session.add(user)
        db.session.commit()

        flash(f'Thank you for signing up Trainer {first_name}!', 'success')
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form=form)
    
@auth.route('/logout')
@login_required
def logout():
    flash('Successfully logged out!', 'warning')
    logout_user()
    return redirect(url_for('main.home'))