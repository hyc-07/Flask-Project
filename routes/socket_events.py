from flask_socketio import emit
from flask_login import current_user
from extensions import db
from models import Message

# ✅ 全局在线用户集合（放在这里最合适）
online_users = set()

def register_socket_events(socketio):

    @socketio.on('connect')
    def handle_connect():
        if current_user.is_authenticated:
            username = current_user.username
            online_users.add(username)
            print(f"✅ 用户 {username} 已连接")
            # ✅ 广播在线用户列表给所有客户端
            emit('online_users', {'users': list(online_users)}, broadcast=True)

    @socketio.on('disconnect')
    def handle_disconnect():
        if current_user.is_authenticated:
            username = current_user.username
            if username in online_users:
                online_users.remove(username)
                print(f"❌ 用户 {username} 断开连接")
                # ✅ 广播在线用户列表给所有客户端
                emit('online_users', {'users': list(online_users)}, broadcast=True)

    @socketio.on('send_message')
    def handle_send_message(data):
        content = data.get('content')

        # 1. 存数据库
        msg = Message(
            user_id=current_user.id,
            content=content
        )
        db.session.add(msg)
        db.session.commit()

        # 2. 广播给所有人
        emit('new_message', {
            'username': current_user.username,
            'content': content,
            "timestamp": msg.beijing_time_str
        }, broadcast=True)