from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Login')

class PkmnForm(FlaskForm):
    pokemon = StringField('Pokemon: ', validators=[DataRequired()])
    submit_pkmn = SubmitField('Submit')

class Signupform(FlaskForm):
    first_name = StringField('First Name: ', validators=[DataRequired()])
    last_name = StringField('Last Name ', validators=[DataRequired()])
    email = EmailField('Email ', validators=[DataRequired()])
    password = PasswordField('Password ', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit_btn = SubmitField('Register')