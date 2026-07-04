# routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import login_user, logout_user, login_required
from extensions import db
from models import User
from forms import RegisterForm

auth = Blueprint("auth", __name__)


# ✅ 注册路由（修改：暂存账号，跳转验证）
@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # 暂存用户名和密码到Session（不立即创建用户）
        session['temp_username'] = form.username.data
        session['temp_password'] = form.password.data
        return redirect(url_for('auth.verify'))  # 跳转到验证页

    return render_template("register.html", form=form)


# ✅ 验证页面路由（渲染test.html）
@auth.route("/verify")
def verify():
    # 无暂存信息则返回注册页
    if 'temp_username' not in session or 'temp_password' not in session:
        flash('请先填写注册信息', 'error')
        return redirect(url_for('auth.register'))
    return render_template("test.html")


# ✅ 验证通过接口（创建用户）
@auth.route("/verify_success", methods=["POST"])
def verify_success():
    # 检查暂存信息
    if 'temp_username' not in session or 'temp_password' not in session:
        return jsonify({'status': 'error', 'message': '验证超时，请重新注册'}), 400

    username = session['temp_username']
    password = session['temp_password']

    # 再次校验用户名唯一性
    if User.query.filter_by(username=username).first():
        session.pop('temp_username', None)
        session.pop('temp_password', None)
        return jsonify({'status': 'error', 'message': '用户名已被占用'}), 400

    # 真正创建用户
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    # 清除暂存信息
    session.pop('temp_username', None)
    session.pop('temp_password', None)

    return jsonify({'status': 'success', 'redirect': url_for('auth.login')})


# （原有login/logout路由保持不变）
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and user.check_password(request.form["password"]):
            login_user(user)
            return redirect(url_for("chat.index"))
        flash('用户名或密码错误', 'error')
        return redirect(url_for('auth.login'))
    return render_template("login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))