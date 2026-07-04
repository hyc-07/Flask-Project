import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")

    # ✅ 优先用环境变量里的 PostgreSQL，没有才 fallback 到 SQLite（本地用）
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///chat.db"
    )

    # Render 新版 PostgreSQL 需要这个
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False