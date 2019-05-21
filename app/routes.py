from app import app, db
from flask import render_template, request, redirect, flash, url_for
from app.forms import LoginForm, RegisterForm, EditProfileForm
from app.models import User, Post
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from datetime import datetime


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        flash("Login requested for user {}".format(request.form['username']))
        user = User.query.filter_by(username=form.username.data).first()
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        if user and user.check_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(next_page)
        flash("Wrong username or password")
        return redirect(url_for('login'))
    return render_template('login.html', form=form, title='Sign in')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if request.method == 'POST' and form.validate_on_submit():
        print("valid")
        _user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(_user)
        db.session.commit()
        flash("You are now registered.")
        return redirect(url_for('login'))

    return render_template('register.html', form=form, title='Register')


@app.route('/user/<username>')
@login_required
def user(username):
    _user = User.query.filter_by(username=username).first_or_404()
    posts = _user.posts
    return render_template('user.html', user=_user, posts=posts, title='My profile')


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form = form, title='Edit profile')
