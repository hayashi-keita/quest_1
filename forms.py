from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')

class RegisterForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), length(min=3, max=20)])
    password = PasswordField('パスワード', validators=[DataRequired(), length(min=6)])
    confirm_password = PasswordField('パスワード確認', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('役割', choices=[('member', '部員'), ('manager', 'マネージャー'), ('coach', 'コーチ'), ('admin', '監督')], default='member')
    grade = SelectField('学年', choices=[('１年', '1'), ('２年', '2'), ('３年', '3'), ('職員', 'teacher')])
    name = StringField('名前', validators=[DataRequired()])
    submit = SubmitField('登録')

class RecordForm(FlaskForm):
    member = SelectField('ユーザー名', coerce=int, validators=[DataRequired()])
    month = StringField('測定月（例：2025-06）', validators=[DataRequired()])
    grade = StringField('学年', validators=[DataRequired()])
    name = StringField('名前', validators=[DataRequired()])
    run_50m = FloatField('50m走 [秒]', validators=[DataRequired()])
    base_running = FloatField('ベースランニング [秒]', validators=[DataRequired()])
    long_throw = FloatField('遠投 [m]', validators=[DataRequired()])
    pitch_speed = FloatField('ストレート球速 [km/h]', validators=[DataRequired()])
    hit_speed = FloatField('打球速度 [km/h]', validators=[DataRequired()])
    swing_speed = FloatField('スイング速度 [km/h]', validators=[DataRequired()])
    bench_press = FloatField('ベンチプレス [kg]', validators=[DataRequired()])
    squat = FloatField('スクワット [kg]', validators=[DataRequired()])
    submit = SubmitField('記録を更新')

class FilterForm(FlaskForm):
    grade = SelectField('学年', choices=[('１年', '１年'), ('２年', '２年'), ('３年', '３年')])
    name = StringField('名前')
    submit = SubmitField('絞り込み')