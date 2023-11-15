from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired



class PkmnForm(FlaskForm):
    pokemon = StringField('Pokemon: ', validators=[DataRequired()])
    submit_pkmn = SubmitField('Submit')