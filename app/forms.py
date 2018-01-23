from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, length


class LoginForm(FlaskForm):
    username = StringField(u'账号', validators=[DataRequired(), length(6, 25, u'账号长度6-25')])
    password = PasswordField(u'密码', validators=[DataRequired(), length(6, 32, u'密码长度6-32')])