# add_user.py
from app import app, db
from models import User
from werkzeug.security import generate_password_hash

with app.app_context():
    users = [
        User(
            username='member',
            password=generate_password_hash('member1234'),
            role='member',
            grade='1',
            name='部員 太郎',
            status='在籍中'
        ),
        User(
            username='manager',
            password=generate_password_hash('manager1234'),
            role='manager',
            grade='2',
            name='記録 登子',
            status='在籍中'
        ),
        User(
            username='coach',
            password=generate_password_hash('coach1234'),
            role='coach',
            grade='teacher',
            name='管 理者',
            status='在籍中'
        ),
        User(
            username='admin',
            password=generate_password_hash('admin1234'),
            role='admin',
            grade='teacher',
            name='監 督者',
            status='在籍中'
        ),
    ]

    db.session.add_all(users)
    db.session.commit()
    print("ユーザーを追加しました")
