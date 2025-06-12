from flask import Blueprint, render_template, request, abort, flash, redirect, url_for
from flask_login import login_required, current_user
from models import Record, User, db
from sqlalchemy.sql import asc, func
from collections import defaultdict
from sqlalchemy import desc
from flask_sqlalchemy import SQLAlchemy

dashboard = Blueprint('dashboard', __name__)

# ダッシュボード作成
@dashboard.route('/dashboard')
@login_required
def show_dashboard():
    if current_user.role not in ['coach', 'admin']:
        flash('このページはアクセスできません。', 'danger')
        return redirect(url_for('index'))

    # 学年ごとの平均値を取得（承認済のみ）
    result = db.session.query(Record.grade,
                              func.avg(Record.run_50m),
                              func.avg(Record.base_running),
                              func.avg(Record.long_throw),
                              func.avg(Record.pitch_speed),
                              func.avg(Record.swing_speed),
                              func.avg(Record.hit_speed),
                              func.avg(Record.bench_press),
                              func.avg(Record.squat)
                            ).filter(Record.coach_approval == True).group_by(Record.grade).all()
    grades = []
    avg_run_50m = []
    avg_base_run = []
    avg_long_throw = []
    avg_pitch = []
    avg_swing = []
    avg_hit = []
    avg_bench = []
    avg_squat = []


    for grade, run_50m, base_run, long_throw, pitch, swing, hit, bench, squat in result:
        grades.append(grade)
        avg_run_50m.append(round(run_50m or 0, 2))
        avg_base_run.append(round(base_run or 0, 2))
        avg_long_throw.append(round(long_throw or 0, 2))
        avg_pitch.append(round(pitch or 0, 2))
        avg_swing.append(round(swing or 0, 2))
        avg_hit.append(round(hit or 0, 2))
        avg_bench.append(round(bench or 0, 2))
        avg_squat.append(round(squat or 0, 2))

    return render_template('dashboard.html',
                            grades=grades, avg_run_50m=avg_run_50m,
                            avg_base_run=avg_base_run, avg_long_throw=avg_long_throw,
                            avg_pitch=avg_pitch, avg_swing=avg_swing,
                            avg_hit=avg_hit, avg_bench=avg_bench, avg_squat=avg_squat)


@dashboard.route('/dashboard/record_progress/<int:user_id>')
@login_required
def record_progress(user_id):
    # ユーザーidで対象選手を取得
    user = User.query.get_or_404(user_id)
    # アクセス制御：自分の記録 or コーチ・監督のみ閲覧
    if current_user.id != user_id and current_user.role not in ['member', 'coach', 'admit']:
        flash('このページにアクセスする権限がありません。', 'danger')
        return redirect(url_for('index'))
    # その選手の記録を日付順に取得（承認済のみ）
    records = Record.query.filter_by(user_id=user_id, coach_approval=True).order_by(Record.month.asc()).all()

    if not records:
        flash('承認済の記録がありません', 'warning')

    dates = [r.month for r in records]
    run_50m = [r.run_50m for r in records]
    base_running = [r.base_running for  r in records]
    long_throw = [r.long_throw for r in records]
    pitch_speed = [r.pitch_speed for r in records]
    swing_speed = [r.swing_speed for r in records]
    hit_speed = [r.hit_speed for r in records]
    bench_press = [r.bench_press for r in records]
    squat = [r.squat for r in records]
    print([r.month for r in records])

    return render_template('dashboard/record_progress.html',
                            user=user, dates=dates, run_50m=run_50m, base_running=base_running,
                            long_throw=long_throw, pitch_speed=pitch_speed,
                            swing_speed=swing_speed, hit_speed=hit_speed,
                            bench_press=bench_press, squat=squat)

@dashboard.route('/dashboard/summary')
@login_required
def dashboard_summary():
    if current_user.role not in ['coach', 'admin']:
        flash('このページはアクセスできません。', 'danger')
        return redirect(url_for('index'))

    # 学年ごとの記録取得・平均処理
    records = Record.query.filter_by(coach_approval=True).all()
    # 学年ごとのリスト初期化（すべての項目を含む）
    grade_data = defaultdict(lambda: {'run_50m': [], 'base_running': [], 'long_throw': [],
                                    'pitch_speed': [], 'swing_speed': [], 'hit_speed': [],
                                    'bench_press': [], 'squat': []})
    for r in records:
        grade = r.grade
        grade_data[grade]['run_50m'].append(r.run_50m)
        grade_data[grade]['base_running'].append(r.base_running)
        grade_data[grade]['long_throw'].append(r.long_throw)
        grade_data[grade]['pitch_speed'].append(r.pitch_speed)
        grade_data[grade]['swing_speed'].append(r.swing_speed)
        grade_data[grade]['hit_speed'].append(r.hit_speed)
        grade_data[grade]['bench_press'].append(r.bench_press)
        grade_data[grade]['squat'].append(r.squat)

    # 平均値計算
    grade_avg = {
        grade:{
            'run_50m': round(sum(vals['run_50m']) / len(vals['run_50m']), 2),
            'base_running': round(sum(vals['base_running']) / len(vals['base_running']), 2),
            'long_throw': round(sum(vals['long_throw']) / len(vals['long_throw']), 2),
            'pitch_speed': round(sum(vals['pitch_speed']) / len(vals['pitch_speed']), 2),
            'swing_speed': round(sum(vals['swing_speed']) / len(vals['swing_speed']), 2),
            'hit_speed': round(sum(vals['hit_speed']) / len(vals['hit_speed']), 2),
            'bench_press': round(sum(vals['bench_press']) / len(vals['bench_press']), 2),
            'squat': round(sum(vals['squat']) / len(vals['squat']), 2)}
            for grade, vals in grade_data.items() if len(vals['run_50m']) > 0}

    grades = sorted(grade_avg.keys())
    avg_run_50m = [grade_avg[g]['run_50m'] for g in grades]
    avg_base_running = [grade_avg[g]['base_running'] for g in grades]
    avg_long_throw = [grade_avg[g]['long_throw'] for g in grades]
    avg_pitch_speed = [grade_avg[g]['pitch_speed'] for g in grades]
    avg_swing = [grade_avg[g]['swing_speed'] for g in grades]
    avg_hit_speed = [grade_avg[g]['hit_speed'] for g in grades]
    avg_bench_press = [grade_avg[g]['bench_press'] for g in grades]
    avg_squat = [grade_avg[g]['squat'] for g in grades]


    return render_template('dashboard/summary.html', grades=grades,
                            avg_run_50m=avg_run_50m, avg_base_running=avg_base_running,
                            avg_long_throw=avg_long_throw, avg_pitch_speed=avg_pitch_speed,
                            avg_swing=avg_swing, avg_hit_speed=avg_hit_speed,
                            avg_bench_press=avg_bench_press, avg_squat=avg_squat)

@dashboard.route('/dashboard/ranking')
@login_required
def ranking():
    if current_user.role not in ['coach', 'admin']:
        flash('このページはアクセスできません。', 'danger')
        return redirect(url_for('index'))

    # 走力ランキング：50m走 + ベースランニング（昇順が良い）
    speed_ranking = Record.query.filter_by(coach_approval=True).order_by(Record.run_50m.asc()).limit(10).all()
    # 肩力ランキング：遠投 + 球速（降順が良い）
    arm_ranking = Record.query.filter_by(coach_approval=True).order_by(desc(Record.long_throw + Record.pitch_speed)).limit(10).all()
    # 打力ランキング：打球速度 + スイング速度（降順）
    hit_ranking = Record.query.filter_by(coach_approval=True).order_by(desc(Record.hit_speed + Record.swing_speed)).limit(10).all()
    # 筋力ランキング：ベンチプレス + スクワット（降順）
    strength_ranking = Record.query.filter_by(coach_approval=True).order_by(desc(Record.bench_press + Record.squat)).limit(10).all()

    return render_template('dashboard/ranking.html',
                            speed_ranking=speed_ranking,
                            arm_ranking=arm_ranking,
                            hit_ranking=hit_ranking,
                            strength_ranking=strength_ranking)

@dashboard.route('/dashboard/record_profile/<int:user_id>')
@login_required
def record_profile(user_id):
    user = User.query.get_or_404(user_id)
    # 最新の承認済の記録を取得
    record = Record.query.filter_by(user_id=user_id, coach_approval=True).order_by(Record.date.asc()).first()
    if not record:
        flash('記録が見つかりません。', 'warning')
        return redirect(url_for('dashboard.dashboard_summary'))

    all_records = Record.query.filter_by(coach_approval=True).all()
    if not all_records:
        flash('平均値を計算できる記録が存在しません。', 'warning')
        return redirect(url_for('dashboard.dashboard_summary'))

    def avg(field):
        values = [getattr(r, field) for r in all_records if getattr(r, field) is not None]
        return round(sum(values) / len(values), 2) if values else 0

    fields = ['run_50m', 'base_running','long_throw', 'pitch_speed',
            'swing_speed', 'hit_speed','bench_press', 'squat']

    data = {'personal': {f: getattr(record, f) for f in fields},
            'team_avg': {f: avg(f) for f in fields}}

    return render_template('dashboard/record_profile.html', user=user, data=data)

# 部員記録検索ページ
@dashboard.route('/dashboard/member_search/', methods=['GET', 'POST'])
@login_required
def member_search():
    if current_user.role not in ['coach', 'admit']:
        flash('アクセス権限がありません。', 'danger')
        return redirect(url_for('index'))

    members = []
    keyword = ''

    if request.method == 'POST':
        keyword = request.form.get('keyword', '').strip()
        if keyword:
            members = User.query.filter(User.role == 'member',
                                        User.name.ilike(f'%{keyword}%')).all()
        else:
            flash('キーワードを入力してください。', 'warning')

    return render_template('dashboard/member_search.html', members=members, keyword=keyword)