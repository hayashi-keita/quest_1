from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models import Record, User
import matplotlib
matplotlib.use('Agg')  # GUI描画を無効化（Flaskでは必須）
import matplotlib.pyplot as plt
import io
import base64
from sqlalchemy import func


dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/my_graph', methods=['GET', 'POST'])
@login_required
def my_graph():
    fields = {'run_50m': '50m走',
              'swing_speed': 'スイング速度',
              'pitch_speed': '投球速度',
              'hit_speed': '打球速度',
              'long_throw': '遠投',
              'bench_press': 'ベンチプレス',
              'squat': 'スクワット'}
    # フォームの情報を取得する（GET）
    select_field = request.form.get('field', 'run_50m')  # デフォルト５０メートル走
    select_user_id = request.form.get('user_id') or current_user.id
    # 表示対象のユーザーを取得
    if current_user.role in ['coach', 'admin']:
        target_user_id = int(select_user_id)
    else:
        target_user_id = current_user.id
    # 対象ユーザーの記録を日付順に取得
    records = Record.query.filter_by(user_id=target_user_id).order_by(Record.date).all()
    # 有効データを抽出
    dates = [r.month for r in records if getattr(r, select_field) is not None]
    values = [getattr(r,select_field) for r in records if getattr(r, select_field) is not None]
    print("dates:", dates)
    print("values:", values)

    # 文字化け防止
    matplotlib.rcParams['font.family'] = 'MS Gothic'
    # グラフ描画
    plt.figure(figsize=(8, 4))
    plt.plot(dates, values, marker='o', label=fields[select_field])
    plt.xlabel('月')
    plt.ylabel(f'{fields[select_field]} の記録推移')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.legend()

    # Base64画像に変換
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    members = []
    if current_user.role in ['coach', 'admin']:
        members = User.query.filter_by(role='member').all()

    return render_template('my_graph.html', graph_url=graph_url, fields=fields, select_field=select_field,
                            members=members, select_user_id=int(select_user_id))

# ダッシュボード作成
@dashboard.route('/dashboard')
@login_required
def show_dashboard():
    role = current_user.role
    context = {'role': role}

    if role == 'member':
        # 自分の記録を取得
        records = Record.query.filter_by(user_id=current_user.id).order_by(Record.date.desc()).all()
        context['records'] = records

    elif role == 'manager':
        # 記録登録リンク用か登録済の記録確認用
        context['register_link'] = True

    elif role == 'coach':
        # 未承認の記録を取得
        pending = Record.query.filter_by(coach_approval=False).all()
        context['pending_record'] = pending
        context['pending_count'] = len(pending)

    elif role == 'admin':
        # 全体統計：承認済数/未承認数
        total = Record.query.count()
        approved = Record.query.filter_by(coach_approval=True).count()
        context['total_records'] = total
        context['approved_records'] = approved
        context['approval_rate'] = round(approved / total * 100, 1) if total > 0 else 0

    return render_template('dashboard.html', **context)