from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, length

class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired()])
    submit = SubmitField('ログイン')

class RegisterForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), length(min=3, max=20)])
    password = StringField('パスワード', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('登録')

class RecordForm(FlaskForm):
    run_50m = FloatField('50m走 [秒]', validators=[DataRequired()])
    base_running = FloatField('ベースランニング [秒]', validators=[DataRequired()])
    long_throw = FloatField('遠投 [m]', validators=[DataRequired()])
    pitch_speed = FloatField('ストレート球速 [km/h]', validators=[DataRequired()])
    hit_speed = FloatField('打球速度 [km/h]', validators=[DataRequired()])
    swing_speed = FloatField('スイング速度 [km/h]', validators=[DataRequired()])
    bench_press = FloatField('ベンチプレス [kg]', validators=[DataRequired()])
    squat = FloatField('スクワット [kg]', validators=[DataRequired()])
    submit = SubmitField('記録を更新！')