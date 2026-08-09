from flask_socketio import emit
from flask_login import current_user
from extensions import db
from models import User, Message

# ✅ 在线用户（用 id，更稳定）
online_user_ids = set()

def register_socket_events(socketio):

    @socketio.on('connect')
    def handle_connect():
        if current_user.is_authenticated:
            online_user_ids.add(current_user.id)
            print(f"✅ 用户 {current_user.username} 已连接")
            emit_user_list(socketio)

    @socketio.on('disconnect')
    def handle_disconnect():
        if current_user.is_authenticated:
            online_user_ids.discard(current_user.id)
            print(f"❌ 用户 {current_user.username} 断开连接")
            emit_user_list(socketio)

    # ✅ 广播【所有用户 + 在线状态 + 头像 + 身份】
    def emit_user_list(socketio):
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

        emit('user_list', {'users': data}, broadcast=True)

    # ✅ 消息发送（携带头像和身份）
    @socketio.on('send_message')
    def handle_send_message(data):
        content = data.get('content')

        msg = Message(
            user_id=current_user.id,
            content=content
        )
        db.session.add(msg)
        db.session.commit()

        # 获取当前用户的头像和身份
        avatar_url = current_user.avatar if current_user.avatar else ""
        user_role = current_user.role if current_user.role else ""

        emit('new_message', {
            'username': current_user.username,
            'content': content,
            'timestamp': msg.beijing_time_str,
            'avatar': avatar_url,
            'role': user_role
        }, broadcast=True)
