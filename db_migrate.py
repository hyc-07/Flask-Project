"""
db_migrate.py —— 一键建表 + 初始化管理员账号
合并原 init_user.py，幂等可重复执行。
"""
import os, sys
from app import create_app
from extensions import db
from models import User, Message

def create_admin(app):
    username = os.environ.get("ADMIN_USERNAME", "hyc")
    password = os.environ.get("ADMIN_PASSWORD", "101007")
    existing = User.query.filter_by(username=username).first()
    if existing:
        print(f"ℹ️  管理员 '{username}' 已存在，跳过")
        return
    admin = User(username=username)
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    print(f"✅ 管理员账号 '{username}' 已创建")

def main():
    app, _ = create_app()
    with app.app_context():
        db.create_all()
        print("✅ 所有数据表已就绪")
        create_admin(app)
    print("🎉 数据库初始化完成")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)