from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)  # 各ユーザーの一意のIDを付ける
    username = db.Column(db.String(150), unique=True, nullable=False)  # ユーザー名、重複を許さない、空も不可
    password = db.Column(db.String(150), nullable=True)  # パスワード、空は不可
    role = db.Column(db.String(50), default='member')
    grade = db.Column(db.String(10))
    name = db.Column(db.String(50))
    status = db.Column(db.String(20), default='在籍中')
    records = db.relationship('Record', backref='user', cascade='all, delete', lazy=True)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.Date, default=datetime.today)
    month = db.Column(db.String(10))
    grade = db.Column(db.String(10))
    name = db.Column(db.String(50))
    run_50m = db.Column(db.Float)
    base_running = db.Column(db.Float)
    long_throw = db.Column(db.Float)
    pitch_speed = db.Column(db.Float)
    hit_speed = db.Column(db.Float)
    swing_speed = db.Column(db.Float)
    bench_press = db.Column(db.Float)
    squat = db.Column(db.Float)
    # 承認フラグ
    member_approval = db.Column(db.Boolean, default=False)
    coach_approval = db.Column(db.Boolean, default=False)
    # 差し戻し理由・フラグ
    reject_reason = db.Column(db.String(255), nullable=True)
    is_rejected = db.Column(db.Boolean, default=False)

# 通知機能
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 通知の宛先
    message = db.Column(db.String(255), nullable=False)  # 通知の内容
    is_read = db.Column(db.Boolean, default=False)  # 既読フラグ
    created_at = db.Column(db.DateTime, default=datetime.now)
    user = db.relationship('User', backref='notifications')

