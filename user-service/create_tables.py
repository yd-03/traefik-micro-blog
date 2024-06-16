from app import create_app, db

# アプリケーションインスタンスの作成
app = create_app()

with app.app_context():
    # テーブルを作成
    db.create_all()
