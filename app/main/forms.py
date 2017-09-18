from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, TextAreaField, BooleanField,\
     SelectField, SelectMultipleField, SubmitField, DateField, RadioField
from wtforms.validators import Required, Length, Email, Regexp, Optional
from wtforms import ValidationError
from ..models import Role, User
from flask_admin.form.widgets import DatePickerWidget
from datetime import datetime


    # class NameForm(FlaskForm):
    #     name = StringField('What is your name?', validators=[Required()])
    #     submit = SubmitField('Submit')


# class EditProfileForm(FlaskForm):
#     name = StringField('Real name', validators=[Length(0, 64)])
#     location = StringField('Location', validators=[Length(0, 64)])
#     about_me = TextAreaField('About me')
#     submit = SubmitField('Submit')


# class EditProfileAdminForm(FlaskForm):
#     email = StringField('Email', validators=[Required(), Length(1, 64),
#                                              Email()])
#     username = StringField('Username', validators=[
#         Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
#                                           'Usernames must have only letters, '
#                                           'numbers, dots or underscores')])
#     confirmed = BooleanField('Confirmed')
#     role = SelectField('Role', coerce=int)
#     name = StringField('Real name', validators=[Length(0, 64)])
#     location = StringField('Location', validators=[Length(0, 64)])
#     about_me = TextAreaField('About me')
#     submit = SubmitField('Submit')

#     def __init__(self, user, *args, **kwargs):
#         super(EditProfileAdminForm, self).__init__(*args, **kwargs)
#         self.role.choices = [(role.id, role.name)
#                              for role in Role.query.order_by(Role.name).all()]
#         self.user = user

#     def validate_email(self, field):
#         if field.data != self.user.email and \
#                 User.query.filter_by(email=field.data).first():
#             raise ValidationError('Email already registered.')

#     def validate_username(self, field):
#         if field.data != self.user.username and \
#                 User.query.filter_by(username=field.data).first():
#             raise ValidationError('Username already in use.')


class PostForm(FlaskForm):
    '''提醒日期不能晚于终止日期'''
    title = StringField("标题：", validators=[Required()])
    summary = TextAreaField("内容摘要：", validators=[Required()])
    note = TextAreaField("备注：")
    depart_id = SelectField("提醒到部门：", coerce=int, default=2,
        # default=User.query.filter_by(username=current_user._get_current_object()).first().get(depart_id), 
        validators=[Required()])
    start_date = DateField("合同开始日期", default='', format='%Y/%m/%d', 
        validators=[Optional()], widget=DatePickerWidget())
    # body = PageDownField("快速添加合同信息：", validators=[Required()])
    end_date = DateField('合同终止日期', default=datetime.now(), 
        validators=[Required()], format='%Y/%m/%d', widget=DatePickerWidget())

    remind_date = DateField('提醒日期', default=datetime.now(), 
        validators=[Required()], format='%Y/%m/%d', widget=DatePickerWidget())
    submit = SubmitField('提交')

class SearchForm(FlaskForm):
    title = StringField("标题：", default=None)
    summary = TextAreaField("内容摘要：", default=None)
    note = TextAreaField("备注：", default=None)
    start_date = DateField("合同开始日期", default=None, format='%Y/%m/%d', 
        validators=[Optional()], widget=DatePickerWidget())
    # body = PageDownField("快速添加合同信息：", validators=[Required()])
    end_date = DateField('合同终止日期', default=None, format='%Y/%m/%d', 
        validators=[Optional()], widget=DatePickerWidget())

    remind_date = DateField('提醒日期', default=None, format='%Y/%m/%d', 
        validators=[Optional()], widget=DatePickerWidget())
    submit = SubmitField('查询')
# class CommentForm(FlaskForm):
#     body = StringField('Enter your comment', validators=[Required()])
#     submit = SubmitField('提交')
