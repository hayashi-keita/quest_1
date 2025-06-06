from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# ログイン処理
@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('record.register_record'))
        else:
            flash('ユーザー名かパスワードが違います')
    return render_template('login.html', form=form)

# ユーザー登録処理
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, password=hash_password,
                    role=form.role.data, grade=form.grade.data, name=form.name.data)
        db.session.add(user)
        db.session.commit()
        flash('登録が完了しました。ログインしてください。')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

# ログアウト処理
@auth.route('/logout')
@login_required  # ログイン済ならアクセス制限
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('auth.login'))