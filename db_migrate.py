from app import app, db
from models import User

def add_columns():
    with app.app_context():
        try:
            db.session.execute('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS realname VARCHAR(80) DEFAULT \'\'')
            db.session.execute('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS bio VARCHAR(200) DEFAULT \'\'')
            db.session.execute('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT \'\'')
            db.session.execute('ALTER TABLE "user" ADD COLUMN IF NOT EXISTS avatar VARCHAR(500) DEFAULT \'\'')
            db.session.commit()
            print("✅ 成功添加新列（realname, bio, role, avatar）")
        except Exception as e:
            db.session.rollback()
            print(f"❌ 添加列失败: {e}")

if __name__ == '__main__':
    add_columns()
