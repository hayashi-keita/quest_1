from app import app  # quest_1ディレクトリ内にある app.py から app を読み込む

# Gunicornが探す変数名は通常 "app"
# Renderでは wsgi:app を呼ぶ → この app 変数がFlaskアプリである必要がある
if __name__ != '__main__':
    application = app