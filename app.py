from flask import Flask
from flask_socketio import SocketIO
from config import Config
from extensions import db, login_manager
from routes.auth import auth
from routes.chat import chat
from models import User
from routes.socket_events import register_socket_events

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # ✅ 生产环境：让 gunicorn + eventlet 接管
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",
        async_mode="gevent"
    )

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth)
    app.register_blueprint(chat)

    with app.app_context():
        db.create_all()

    register_socket_events(socketio)

    return app, socketio

app, socketio = create_app()
