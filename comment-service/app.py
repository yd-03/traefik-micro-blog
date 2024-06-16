from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@db:5432/user_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    author_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


@app.route("/comments", methods=["POST"])
def create_comment():
    data = request.get_json()
    new_comment = Comment(
        post_id=data["post_id"], author_id=data["author_id"], content=data["content"]
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify(
        {
            "id": new_comment.id,
            "post_id": new_comment.post_id,
            "author_id": new_comment.author_id,
            "content": new_comment.content,
        }
    ), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
