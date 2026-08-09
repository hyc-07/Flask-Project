from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models import User, Message

chat = Blueprint("chat", __name__)

@chat.route("/")
@chat.route("/chat")
@login_required
def index():
    return render_template("chat.html")

@chat.route("/history")
@login_required
def history():
    """返回历史消息列表，包含头像和身份信息"""
    messages = Message.query.order_by(Message.timestamp.asc()).all()
    result = []
    for m in messages:
        user = User.query.get(m.user_id)
        avatar_url = user.avatar if user and user.avatar else ""
        user_role = user.role if user and user.role else ""
        result.append({
            'username': user.username if user else '未知',
            'content': m.content,
            'timestamp': m.beijing_time_str,
            'avatar': avatar_url,
            'role': user_role
        })
    return jsonify(result)

@chat.route("/online_users")
@login_required
def online_users():
    """返回所有用户列表（含在线状态、头像、身份）"""
    from routes.socket_events import online_user_ids

    users = User.query.all()
    data = []
    for u in users:
        data.append({
            "id": u.id,
            "username": u.username,
            "online": u.id in online_user_ids,
            "realname": u.realname if u.realname else "",
            "role": u.role if u.role else "",
            "avatar": u.avatar if u.avatar else "",
            "bio": u.bio if u.bio else ""
        })
    return jsonify({"users": data})

@chat.route("/update_profile", methods=["POST"])
@login_required
def update_profile():
    """更新当前用户的真实姓名、头像、简介"""
    data = request.get_json()
    realname = data.get('realname', '').strip()
    bio = data.get('bio', '').strip()
    avatar = data.get('avatar', '').strip()

    if not realname:
        return jsonify({"success": False, "message": "真实姓名不能为空"}), 400

    current_user.realname = realname
    current_user.bio = bio
    if avatar:
        current_user.avatar = avatar

    db.session.commit()
    return jsonify({"success": True})
