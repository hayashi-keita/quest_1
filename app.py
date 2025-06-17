
    # .venv\Scripts\activate
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_migrate import Migrate, upgrade
import sys
import os
sys.path.append(os.path.dirname(__file__))
from models import db, User, Notification, Record  # ユーザー情報などの「データ構造」（Userモデル）を定義している別ファイル models.py から読み込む
from routes.auth import auth  # Blueprint（routes.py内）で定義したルーティングを使えるようにする
from routes.record import record
from routes.user import user
from routes.dashboard import dashboard
from routes.notification import notification


app = Flask(__name__)  # __name__はこのファイルが実行されるときの名前
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')  # フォームなどのセキュリティー用のキー
# SQLite（ローカル用）とPostgreSQL（Render用）を切り替えられるようにする
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///team_data.db')  # データベースの保存場所を指定
print("DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])

db.init_app(app)  # FlaskとSQLAlchemyを接続し、DB操作できるようにする
migrate = Migrate(app, db)

login_manager = LoginManager(app)  # ログイン状態を管理する仕組みを初期化
login_manager.login_view = 'auth.login'  # ログインが必要なページにアクセスしたときに login という関数のURLにリダイレクトする設定

@login_manager.user_loader  # Flask-Loginが「今ログインしている人」を取得する方法を定義
def load_user(user_id):
    return User.query.get(int(user_id))  # データベースから user_id に一致するユーザーを探して返す

@app.context_processor
def inject_notification_count():
    if current_user.is_authenticated:
        cnt = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
        print(f"未読通知数: {cnt}")
    else:
        cnt = 0
    return dict(notification_count=cnt)

# Blueprint の登録
app.register_blueprint(auth)  # Flask アプリにルートを登録（登録しないと /login などが使えない）
app.register_blueprint(record)
app.register_blueprint(user)
app.register_blueprint(dashboard)
app.register_blueprint(notification)

# テーブル作成
# with app.app_context():
    # db.create_all()

# トップページにアクセスされたとき、自動的にログインページにリダイレクトする関数
@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/healthz')
def healthz_check():
    return 'OK', 200


# with app.app_context():
    # from flask_migrate import upgrade
    # upgrade()


if __name__ == '__main__':  # このファイルが直接実行されたときだけ、アプリを起動
    app.run(debug=True)  # debug=True にすると変更が即時反映され、エラーも詳しく表示される