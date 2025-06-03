from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime
from forms import RecordForm
from models import db, Record, User

# 記録画面登録
record = Blueprint('record', __name__)

@record.route('/record', methods=['GET', 'POST'])
def register_record():
    form = RecordForm()
    if form.validate_on_submit():
        new_record = Record(user_id=current_user.id,
                            date=datetime.now().date(),
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


@record.route('/records')
@login_required
def view_records():
    records = Record.query.filter_by(user_id=current_user.id).order_by(Record.date.desc()).all()
    return render_template('record_list.html', records=records)


@record.route('/all_records')
@login_required
def all_records():
    if current_user.role == 'member':
        flash('アクセス権限がありません。', 'danger')
        return redirect(url_for('index'))

    records = Record.query.order_by(Record.date.desc()).all()
    users = {user.id: user.username for user in User.query.all()}
    return render_template('all_records.html', records=records, users=users)

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

# コート承認ボタンのPOST処理
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



