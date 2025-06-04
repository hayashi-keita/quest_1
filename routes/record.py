from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from forms import RecordForm, FilterForm
from models import db, Record, User
import matplotlib
matplotlib.use('Agg')  # GUI描画を無効化（Flaskでは必須）
import matplotlib.pyplot as plt
import io
import base64

# 記録画面登録
record = Blueprint('record', __name__)

@record.route('/record', methods=['GET', 'POST'])
@login_required
def register_record():
    if current_user.role != 'manager':
        flash('このページにアクセスする権限がありません。')
        return redirect(url_for('auth.login'))

    form = RecordForm()
    if form.validate_on_submit():
        new_record = Record(user_id=current_user.id,
                            date=datetime.now().date(),
                            month = form.month.data,
                            grade = form.grade.data,
                            name = form.name.data,
                            run_50m=form.run_50m.data,
                            base_running=form.base_running.data,
                            long_throw=form.long_throw.data,
                            pitch_speed=form.pitch_speed.data,
                            hit_speed=form.hit_speed.data,
                            swing_speed=form.swing_speed.data,
                            bench_press=form.bench_press.data,
                            squat= form.squat.data
        )
        db.session.add(new_record)
        db.session.commit()
        flash('記録を登録しました。')
        return redirect(url_for('record.register_record'))

    return render_template('record.html', form=form)

# ログイン中部員の記録
@record.route('/records')
@login_required
def view_records():
    records = Record.query.filter_by(user_id=current_user.id).order_by(Record.date.desc()).all()
    return render_template('record_list.html', records=records)

# 全部員の記録
@record.route('/all_records')
@login_required
def all_records():
    if current_user.role == 'member':
        flash('アクセス権限がありません。', 'danger')
        return redirect(url_for('index'))

    form = FilterForm()
    query = Record.query.join(User)  # データベースからユーザー名を検索し結合

    if form.validate_on_submit():
        if form.grade.data:
            query = query.filter(User.grade == form.grade.data)
        if form.name.data:
            query =query.filter(User.name.contains(form.name.data))

    records = Record.query.order_by(Record.date.desc()).all()
    users = {user.id: user.username for user in User.query.all()}
    return render_template('all_records.html', records=records, users=users)

# 部員の承認ページ
@record.route('/my_approvals', methods=['GET', 'POST'])
@login_required
def my_approvals():
    #部員の記録を取得
    records = Record.query.filter_by(user_id=current_user.id).order_by(Record.date.desc()).all()
    return render_template('my_approvals.html', records=records)

# コーチだけの承認ページ
@record.route('/coach_approvals')
@login_required
def coach_approvals():
    if current_user.role != 'coach':
        flash('アクセス権限がありません。', 'danger')
        return redirect(url_for('index'))

    records = Record.query.filter_by(member_approval=True, coach_approval=False).order_by(Record.date.desc()).all()
    users = {user.id: user.username for user in User.query.all()}
    return render_template('coach_approvals.html', records=records, users=users)

# コーチ承認ボタンのPOST処理
@record.route('/approve_by_coach/<int:record_id>', methods=['POST'])
@login_required
def approve_by_coach(record_id):
    if current_user.role != 'coach':
        flash('アクセス権限がありません。', 'danger')
        return redirect(url_for('index'))

    records = Record.query.get_or_404(record_id)
    records.coach_approval = True
    db.session.commit()
    flash('記録を最終承認しました。', 'success')
    return redirect(url_for('record.coach_approvals'))

# 部員承認ボタンのPOST処理
@record.route('/approve_by_member/<int:record_id>', methods=['POST'])
@login_required
def approve_by_member(record_id):
    if current_user.role != 'member':
        flash('アクセス権限がありません。', 'danger')
        return redirect(url_for('index'))

    records = Record.query.get_or_404(record_id)
    if current_user.id != records.user_id:
        flash('他人の記録は承認できません。', 'danger')
        return redirect(url_for('record.my_approvals'))

    records.member_approval = True
    db.session.commit()
    flash('記録を承認しました。', 'success')
    return redirect(url_for('record.my_approvals'))

# グラフ表示処理
@record.route('/user_chart/<int:user_id>/<string:field>')
@login_required
def user_chart(user_id, field):
    records = Record.query.filter_by(user_id=user_id).order_by(Record.date).all()
    dates = [r.date.strftime('%Y-%m-%d') for r in records]
    values = [getattr(r, field) for r in records]

    field_names = {'hit_speed': '打球速度', 'pitch_speed': '投球速度', 'swing_speed': 'スウィング速度',
                   'run_50m': '50m走', 'bench_press': 'ベンチプレス', 'squat': 'スクワット'}
    field_jp = field_names.get(field, field)

    plt.rcParams['font.family'] = 'MS Gothic'  # フォント設定 IPAexGothic

    plt.figure(figsize=(8, 4))
    plt.plot(dates, values, marker='o')
    plt.title(f'{field_jp}の推移')
    plt.xlabel('日付')
    plt.ylabel(field_jp)
    plt.xticks(rotation=45)
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()

    return render_template('user_chart.html', graph_url=graph_url,
                            user=User.query.get(user_id), field=field, field_jp=field_jp)



