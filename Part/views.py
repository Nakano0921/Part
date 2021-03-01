from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user

from Part.forms import LoginForm, RegisterForm, RegisterForm_R
from Part.models import User
from Part.models import RestaurantUser

bp = Blueprint('app', __name__ , url_prefix='')

@bp.route('/')
def home():
    return render_template('home.html')

@bp.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@bp.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('app.home'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_by_email(form.email.data)
        if user and user.validate_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if not next:
                next = url_for('app.welcome')
            return redirect(next)
    return render_template('login.html', form=form)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            email = form.email.data,
            username = form.username.data,
            password = form.password.data
        )
        user.add_user()
        return redirect(url_for('app.login'))
    return render_template('signup.html', form=form)

@bp.route('/user')
@login_required
def user():
    return render_template('user.html')

@bp.route('/r_login', methods=['GET', 'POST'])
def r_login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        restaurantuser = RestaurantUser.select_by_email(form.email.data)
        if restaurantuser and restaurantuser.validate_password(form.password.data):
            login_user(restaurantuser)
            next = request.args.get('next')
            if not next:
                next = url_for('app.welcome')
            return redirect(next)
    return render_template('r-login.html', form=form)

@bp.route('/r_signup', methods=['GET', 'POST'])
def r_signup():
    form = RegisterForm_R(request.form)
    if request.method == 'POST' and form.validate():
        restaurantuser = RestaurantUser(
            email = form.email.data,
            representative = form.representative.data,
            password = form.password.data
        )
        restaurantuser.add_user()
        return redirect(url_for('app.r_login'))
    return render_template('r-signup.html', form=form)

@bp.route('/restaurant')
@login_required
def restaurant():
    return render_template('restaurant.html')