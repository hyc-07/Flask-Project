# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from models import User
from extensions import db

class RegisterForm(FlaskForm):
    username = StringField(
        '用户名',
        validators=[
            DataRequired(message='用户名不能为空'),
            Length(min=3, max=20, message='用户名长度3-20位')
        ]
    )
    password = PasswordField(
        '密码',
        validators=[
            DataRequired(message='密码不能为空'),
            Length(min=6, message='密码至少6位')
        ]
    )
    confirm_password = PasswordField(
        '确认密码',
        validators=[
            DataRequired(message='请确认密码'),
            EqualTo('password', message='两次密码不一致')
        ]
    )
    submit = SubmitField('注册')

    # ✅ 自定义验证器：检查用户名是否已存在
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('该用户名已被占用')