from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from marshmallow import Schema, fields, validate, ValidationError

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    # データベース設定: PostgreSQL
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@db:5432/user_db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    # Userモデルの定義
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)  # ユーザーID
        name = db.Column(db.String(255), nullable=False)  # ユーザー名
        email = db.Column(db.String(255), unique=True, nullable=False)  # メールアドレス
        password_hash = db.Column(
            db.String(255), nullable=False
        )  # パスワードのハッシュ
        created_at = db.Column(
            db.DateTime, default=db.func.current_timestamp()
        )  # 作成日時
        updated_at = db.Column(
            db.DateTime,
            default=db.func.current_timestamp(),
            onupdate=db.func.current_timestamp(),
        )  # 更新日時

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)

    # ユーザースキーマの定義
    class UserSchema(Schema):
        name = fields.String(required=True, validate=validate.Length(min=1, max=255))
        email = fields.Email(required=True)
        password = fields.String(required=True, validate=validate.Length(min=6))

    user_schema = UserSchema()

    # ユーザー登録のエンドポイント
    @app.route("/users/register", methods=["POST"])
    def register_user():
        try:
            data = request.get_json()  # リクエストデータの取得
            user_schema.load(data)  # データのバリデーション
            new_user = User(
                name=data["name"], email=data["email"]
            )  # 新しいユーザーオブジェクトの作成
            new_user.set_password(data["password"])  # パスワードのハッシュ化
            db.session.add(new_user)  # データベースセッションに追加
            db.session.commit()  # データベースにコミット
            return jsonify(
                {"id": new_user.id, "name": new_user.name, "email": new_user.email}
            ), 201  # レスポンスとしてユーザー情報を返す
        except ValidationError as ve:
            return jsonify({"errors": ve.messages}), 400
        except IntegrityError:
            db.session.rollback()
            return jsonify({"error": "Email already exists"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)  # アプリケーションの実行
