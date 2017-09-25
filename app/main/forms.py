from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_login import current_user
from wtforms import StringField, TextAreaField, BooleanField,\
     SelectField, SelectMultipleField, SubmitField, DateField, RadioField
from wtforms.validators import Required, Length, Email, Regexp, Optional
from wtforms import ValidationError
from ..models import Role, User
from flask_admin.form.widgets import DatePickerWidget
from datetime import datetime


class PostForm(FlaskForm):
    title = StringField("标题：", validators=[Required()])
    summary = TextAreaField("内容摘要：", validators=[Required()])
    note = TextAreaField("备注：")
    depart_id = SelectField("所属部门：", coerce=int, default=0,
        # default=User.query.filter_by(username=current_user._get_current_object()).first().get(depart_id),
        validators=[Required()])
    start_date = DateField("合同开始日期：", default='', format='%Y/%m/%d',
        validators=[Optional()], widget=DatePickerWidget())
    # body = PageDownField("快速添加合同信息：", validators=[Required()])
    end_date = DateField('合同终止日期：', default=datetime.now(),
        validators=[Required()], format='%Y/%m/%d', widget=DatePickerWidget())

    remind_date = DateField('提醒日期：', default=datetime.now(),
        validators=[Required()], format='%Y/%m/%d', widget=DatePickerWidget())
    submit = SubmitField('提交')

class SearchForm(FlaskForm):
    title = StringField("标题：", default=None)
    summary = TextAreaField("内容摘要：", default=None)
    note = TextAreaField("备注：", default=None)
    depart_id = SelectField("所属部门：", coerce=int, default=0,
        validators=[Optional()])
    start_date = DateField("合同开始日期：", default=None, format='%Y/%m/%d',
        validators=[Optional()], widget=DatePickerWidget())
    # body = PageDownField("快速添加合同信息：", validators=[Required()])
    end_date = DateField("合同终止日期：", default=None, format='%Y/%m/%d',
        validators=[Optional()], widget=DatePickerWidget())

    remind_date = DateField('提醒日期：', default=None, format='%Y/%m/%d',
        validators=[Optional()], widget=DatePickerWidget())
    submit = SubmitField('查询')


class AttachForm(FlaskForm):
    attach = FileField('导入数据：', validators=[FileRequired(),
        FileAllowed(['xls'], message=u'仅支持.xls格式(Excel 97-03格式)')])
    # submit = SubmitField('上传')
