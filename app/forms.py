from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, length, email, EqualTo


class LoginForm(FlaskForm):
    username = StringField(u'账号', validators=[DataRequired(message=u'账号未填'), length(6, 25, u'账号长度6-25')])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'密码未填'), length(6, 32, u'密码长度6-32')])

class SignForm(FlaskForm):
    username = StringField(u'账号', validators=[DataRequired(message=u'账号未填'), length(6, 25, u'账号长度6-25')])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'密码未填'), length(6, 32, u'密码长度6-32'), EqualTo('confirm', '')])
    confirm = PasswordField(u'确认密码')
    email = StringField(u'邮箱', validators=[DataRequired(message=u'邮箱未填'), email(u'邮箱格式错误')])

class ArticleForm(FlaskForm):
    title = StringField(u'文章标题', validators=[DataRequired(message=u'标题未填'), length(min=1, max=80, message=u'标题最大长度80')])
    content = TextAreaField(u'内容', validators=[DataRequired()])
    #tag = StringField(u'标签')