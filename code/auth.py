from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
  if request.method == 'POST':
    email = request.form.get("email")
    password = request.form.get("password")

    user_exists = User.query.filter_by(email=email).first()

    if user_exists:
      if check_password_hash(user_exists.password, password):
        flash('Logged in!', category='success!')
        login_user(user_exists, remember=True)
        return redirect(url_for('views.home'))
      else:
        flash('Password is Incorrect.', category='error')
    else:
      flash('Email does not exist!', category='error')
  return render_template("login.html")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
  if request.method == "POST":
    email = request.form.get("email")
    username = request.form.get("username")
    password1 = request.form.get("password1")

    email_exists = User.query.filter_by(email=email).first()
    username_exists = User.query.filter_by(username=username).first()
    if email_exists:
      flash('EMAIL IS IN USE!', category='error') # Flashes message on the screen.
    elif username_exists:
      flash('USERNAME IS IN USE!', category='error')
    elif len(username) < 2:
      flash('USERNAME IS TOO SHORT!', category='error')
    elif len(password1) < 2:
      flash('PASSWORD IS TOO SHORT!', category='error')
    elif len(email) < 4:
      flash('EMAIL IS INVALID!', category='error')
    else:
      new_user = User(email=email, username=username, password=generate_password_hash(password1, method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True)
      flash('USER CREATED!!')
      return redirect(url_for('views.home'))
  return render_template("signup.html")

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
  if request.method == "POST":
    pass
  return render_template("forgot_password.html")

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('views.begin'))


