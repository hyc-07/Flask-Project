from app import create_app
from extensions import db
from models import User

app, _ = create_app()

with app.app_context():
    if not User.query.filter_by(username="hyc").first():
        u = User(username="hyc")
        u.set_password("101007")
        db.session.add(u)
        db.session.commit()
        print("✅ 管理员创建成功")
    else:
        print("ℹ️ 管理员已存在")