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
        .order_by(Message.timestamp.asc())
        .limit(70)
        .all()
    )

    data = []
    for m in messages:
        data.append({
            "username": m.user.username,
            "content": m.content,
            "timestamp": m.beijing_time_str
        })

    return jsonify(data)