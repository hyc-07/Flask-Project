# models.py
from extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(200))

    def set_password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def check_password(self, pwd):
        return check_password_hash(self.password_hash, pwd)
    # ✅ 新增字段
    real_name = db.Column(db.String(50))      # 真实姓名
    bio = db.Column(db.Text)                  # 个人介绍
    status = db.Column(db.String(20), default='😊 在线')  # 在线状态

    messages = db.relationship('Message', backref='user', lazy=True)

    @property
    def is_online(self):
        from socket_events import online_user_ids
        return self.id in online_user_ids

# models.py
from datetime import datetime
import pytz

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='messages')

    # ✅ 新增：返回 UTC+8 时间字符串
    @property
    def beijing_time_str(self):
        beijing = pytz.timezone("Asia/Shanghai")
        local_time = self.timestamp.replace(tzinfo=pytz.utc).astimezone(beijing)
        return local_time.strftime("%m-%d %H:%M")
