from flask import Flask, render_template
from flask_socketio import SocketIO  # ✅ 新增
from config import Config
from extensions import db, login_manager
from routes.auth import auth
from routes.chat import chat
from models import User  # ✅ 必须导入
from routes.socket_events import register_socket_events


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # ✅ 初始化 SocketIO
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

    # ✅ user_loader（必须保留）
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth)
    app.register_blueprint(chat)

    with app.app_context():
        db.create_all()

    # ✅ 返回 app 和 socketio
    return app, socketio

app, socketio = create_app()
register_socket_events(socketio)

if __name__ == "__main__":
    # ✅ 用 socketio.run 启动
    socketio.run(app, host="0.0.0.0", port=5050, debug=True)