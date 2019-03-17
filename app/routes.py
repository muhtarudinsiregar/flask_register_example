from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import app
from app.forms import LoginForm, RegisterForm
from app.models import User


@app.route('/index')
@login_required
def index():
    posts = []
    return render_template("index.html", title="Homepage", posts=posts)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))

    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template("register.html", title="Sign Up", form=form)
