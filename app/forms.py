from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class PkmnForm(FlaskForm):
    pokemon = StringField('Pokemon: ', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')