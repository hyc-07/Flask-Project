import os
from urllib.parse import urlparse


def _build_engine_options(database_url: str) -> dict:
    """根据 Supabase 连接串类型，智能返回 SQLAlchemy 引擎选项。"""
    parsed = urlparse(database_url)
    port = parsed.port

    # Supabase Transaction Pooler 走 6543 端口，必须用 NullPool
    if port == 6543:
        from sqlalchemy.pool import NullPool
        return {"poolclass": NullPool}

    # Session Pooler / 直连：保守配置 + 防断线
    return {
        "pool_size": 2,
        "max_overflow": 2,
        "pool_timeout": 30,
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-me"

    # ── 数据库 URI ──
    database_url = os.environ.get("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = database_url or "sqlite:///chat.db"

    # ── 引擎选项（仅 PostgreSQL） ──
    if database_url:
        SQLALCHEMY_ENGINE_OPTIONS = _build_engine_options(database_url)

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 生产环境建议 False，由 db_migrate.py 管理表结构
    AUTO_CREATE_DB = os.environ.get("AUTO_CREATE_DB", "False") == "True"