#!/bin/bash
# init_db.sh —— 本地一键初始化 Supabase 数据库
# 用法: bash init_db.sh

set -e

echo "🔧 Flask-Project 数据库初始化脚本"
echo "=================================="

# ── 检查是否设置了 DATABASE_URL ──────────────────────────────
if [ -z "$DATABASE_URL" ]; then
    echo "⚠️  未检测到 DATABASE_URL 环境变量"
    echo ""
    echo "请先设置你的 Supabase Transaction Pooler 连接串："
    echo ""
    echo "  export DATABASE_URL=\"postgresql://postgres.xxxx:密码@aws-0-ap-southeast-1.pooler.supabase.com:5432/postgres\""
    echo ""
    echo "或者复制 .env.example 为 .env 并填入后执行："
    echo "  set -a; source .env; set +a"
    echo ""
    echo "继续使用本地 SQLite (sqlite:///chat.db) ? [y/N]"
    read -r ans
    if [ "$ans" != "y" ] && [ "$ans" != "Y" ]; then
        echo "已取消"
        exit 1
    fi
    export DATABASE_URL="sqlite:///chat.db"
fi

echo "📡 使用数据库: $DATABASE_URL"
echo ""

# ── 安装依赖 ─────────────────────────────────────────────────
echo "📦 检查依赖..."
pip install -q psycopg2-binary 2>/dev/null || true

# ── 执行迁移 ─────────────────────────────────────────────────
echo "🚀 开始初始化..."
python db_migrate.py

echo ""
echo "✅ 完成！现在可以 git push 触发 Render 部署"
