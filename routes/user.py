from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import User, db
from functools import wraps

user = Blueprint('user', __name__)

# 権限チェック用（コーチ・監督のみ許可）
def coach_or_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role not in ['coach', 'admin']:
            flash('アクセス権限がありません。', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# 部員管理画面表示（一覧と作成フォーム）
@user.route('/manage_members', methods=['GET', 'POST'])
@login_required
@coach_or_admin_required
def manage_members():
    if request.method == 'POST':
        # 新規部員作成処理
        username = request.form.get('username')
        grade = request.form.get('grade')
        name = request.form.get('name')
        role = 'member'  # 部員はrole=member固定
        # 簡易バリデーション
        if not username:
            flash('ユーザー名は必須です。', 'warning')
        elif not grade:
            flash('学年入力は必須です。', 'warning')
        elif not name:
            flash('名前入力は必須です', 'warning')
        else:
            existing = User.query.filter_by(username=username).first()
            if existing:
                flash('そのユーザー名は既に存在します。' 'warning')
            else:
                new_user = User(username=username, grade=grade, name=name, role=role)
                # 必要ならここでパスワード設定
                db.session.add(new_user)
                db.session.commit()
                flash(f'部員「{username}」学年「{grade}」を作成しました。', 'success')
                return redirect(url_for('user.manage_members'))

    # 部員一覧（退部・引退処理用にステータス項目などあれば追加）
    members = User.query.filter_by(role='member').all()
    return render_template('manage_members.html', members=members)

# 部員の退部・引退ステータス更新処理
@user.route('/manage_members/<int:user_id>/update_status', methods=['POST'])
@login_required
@coach_or_admin_required
def update_member_status(user_id):
    user = User.query.get_or_404(user_id)
    action = request.form.get('action')

    if action == '退部':
        # 退部処理例（ステータスフラグを変えるなど）
        user.status = '退部'
        flash(f'{user.username}さんを退部扱いにしました。', 'success')
    elif action == '引退':
        # 退会などの処理
        user.status = '引退'
        flash(f'{user.username}さんを引退扱いにしました。', 'success')
    elif action == '在籍中':
        # 退会などの処理
        user.status = '在籍中'
        flash(f'{user.username}さんを在籍扱いにしました。', 'success')
    else:
        flash('不正な操作です。', 'danger')

    db.session.commit()
    return redirect(url_for('user.manage_members'))


