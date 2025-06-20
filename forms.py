from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, length, EqualTo

class LoginForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired()], render_kw={'autocomplete': 'off'})
    password = PasswordField('パスワード', validators=[DataRequired()], render_kw={'autocomplete': 'new-password'})
    submit = SubmitField('ログイン')

class RegisterForm(FlaskForm):
    username = StringField('ユーザー名', validators=[DataRequired(), length(min=3, max=20)], render_kw={'autocomplete': 'off'})
    password = PasswordField('パスワード', validators=[DataRequired(), length(min=6)], render_kw={'autocomplete': 'new-password'})
    confirm_password = PasswordField('パスワード確認', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('役割', choices=[('', '選択してください'), ('member', '部員'), ('manager', 'マネージャー'), ('coach', 'コーチ'), ('admin', '監督')])
    grade = SelectField('学年', choices=[('', '選択してください'), ('1', '1'), ('2', '2'), ('3', '3'), ('職員', 'teacher')])
    name = StringField('名前', validators=[DataRequired()])
    submit = SubmitField('登録')

class RecordForm(FlaskForm):
    member = SelectField('ユーザー名', coerce=int, validators=[DataRequired()], choices=[(0, '選択してください')])
    month = StringField('測定月（例：2025-06）', validators=[DataRequired()])
    grade = SelectField('学年', choices=[('', '選択してください'), ('1', '1'), ('2', '2'), ('3', '3')])
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
    grade = SelectField('学年', choices=[('', '選択してください'), ('0', '全て'), ('1', '1'), ('2', '2'), ('3', '3')])
    name = StringField('名前')
    submit = SubmitField('絞り込み')

class RejectForm(FlaskForm):
    reject_reason = StringField('差し戻し理由', validators=[DataRequired()])
    submit = SubmitField('差し戻す')