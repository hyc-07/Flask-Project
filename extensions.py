from flask import redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

login_manager.login_view = "auth.login"
@login_manager.unauthorized_handler
def unauthorized():
    # 直接跳转到登录页，不返回任何提示文字
    return redirect(url_for('auth.login'))