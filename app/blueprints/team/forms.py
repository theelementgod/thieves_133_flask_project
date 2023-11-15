from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField

class TeamForm(FlaskForm):
    pokemon1 = StringField('Pokemon #1: ')
    pokemon2 = StringField('Pokemon #2: ')
    pokemon3 = StringField('Pokemon #3: ')
    pokemon4 = StringField('Pokemon #4: ')
    pokemon5 = StringField('Pokemon #5: ')
    pokemon6 = StringField('Pokemon #6: ')
    submit_btn = SubmitField('Register')