from flask import Blueprint, render_template
from flask_login import login_required

chat = Blueprint("chat", __name__)

@chat.route("/")
@login_required
def index():
    return render_template("chat.html")

from flask import jsonify
from flask_login import login_required
from models import Message

@chat.route("/history")
@login_required
def chat_history():
    messages = (
        Message.query
        .order_by(Message.timestamp.desc())  # ✅ 先取最新的120条（从新到旧）
        .limit(120)
        .all()
    )
    messages.reverse()

    data = []
    for m in messages:
        data.append({
            "username": m.user.username,
            "content": m.content,
            "timestamp": m.beijing_time_str
        })

    return jsonify(data)


from flask import jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models import Message, User


@chat.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    data = request.get_json()

    realname = data.get('realname', '').strip()
    bio = data.get('bio', '').strip()

    if not realname:
        return jsonify({"success": False, "message": "真实姓名不能为空"}), 400

    current_user.realname = realname
    current_user.bio = bio

    try:
        db.session.commit()
        return jsonify({"success": True, "message": "更新成功"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": "服务器错误"}), 500
