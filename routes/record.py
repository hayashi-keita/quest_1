from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import datetime
from forms import RecordForm
from models import db, Record

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

@record.route('/dashboard.html')
@login_required
def dashboard():
    return redirect(url_for('record.register_record'))
