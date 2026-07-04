from app import create_app
from extensions import db
from models import User

# ✅ 解包元组
app, socketio = create_app()

with app.app_context():
    if not User.query.filter_by(username="admin2").first():
        u = User(username="admin2")
        u.set_password("123456")
        db.session.add(u)
        db.session.commit()
        print("✅ 管理员账号创建成功：admin / 123456")
    else:
        print("ℹ️ 账号已存在")