from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    SelectField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('保持登录状态')
    submit = SubmitField('登录')


class RegistrationForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('[A-Za-z0-9\u4e00-\u9fa5_@.]+', 0,
                                          '用户名只能包含汉字 大小写字母 _ @ .')])            
    password = PasswordField('输入密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('重复密码', validators=[Required()])
    depart_id = SelectField('所在部门', coerce=int, default=2, 
                            validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被注册')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='两次输入须一致')])
    password2 = PasswordField('确认密码', validators=[Required()])
    submit = SubmitField('更新密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('重置密码')


class PasswordResetForm(FlaskForm):
    email = StringField('邮箱', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('重复密码', validators=[Required()])
    submit = SubmitField('重置密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('未知的邮箱地址')


class ChangeEmailForm(FlaskForm):
    email = StringField('新邮箱', validators=[Required(message='邮箱地址不能为空'), 
        Length(1, 64), Email()])
    password = PasswordField('密码', validators=[Required(message='密码不能为空')])
    submit = SubmitField('更新邮箱')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('邮箱已被注册')


class CopyEmailForm(FlaskForm):
    email2 = StringField('待抄送邮箱', validators=[Required(message='邮箱地址不能为空'), Length(1, 64),
        Email()])
    password = PasswordField('验证密码', validators=[Required(message='密码不能为空')])
    submit = SubmitField('更新抄送邮箱')

    def validate_email2(self, field):
        if field.data == current_user.email:
            raise ValidationError('不能抄送给自己')