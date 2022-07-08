from calendar import c
from flask import Blueprint, render_template, request, flash, redirect, url_for
import time
from .models import *
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('email')
        email = email.lower()
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if len(email) == 0:
            flash(f'Please enter an email address', category="error")

        elif user:
            if check_password_hash(user.password, password):
                flash(f'Welcome back, {user.first_name}!', category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Invalid credentials.", category='error')
        else:
            flash("Invalid credentials.", category="error")

    if current_user.is_authenticated == True:
        return redirect(url_for("views.home"))
    else:
        return render_template("login.html", user=current_user)


@auth.route('/logout')
def logout():
    if current_user.is_authenticated == True:
        logout_user()
        return redirect(url_for("auth.login"))
    else:
        return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        email = email.lower()
        first_name = request.form.get('first_name')
        first_name = first_name.lower().capitalize()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('This email already exists.', category='error')

        elif len(email) < 4:
            flash('Email must have more than 3 characters.', category='error')

        elif len(first_name) is 0:
            flash('Please enter your first name. ', category='error')

        elif len(password1) < 8:
            flash('Password should have at least 8 characters.', category='error')

        elif password1 != password2:
            flash('Passwords do not match.', category='error')

        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256')
                            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Your account has been created. 👍', category='success')

            return redirect(url_for('views.home'))

    return render_template("sign-up.html", user=current_user)
