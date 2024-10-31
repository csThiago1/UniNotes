from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField, validators

class LoginForm(FlaskForm):
    user_id = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=20)])
    password = PasswordField('Senha', [validators.DataRequired(), validators.Length(min=1, max=100)])
    login = SubmitField('Login')