from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired

class PkmnForm(FlaskForm):
    pkmn_name = StringField('Enter Pokémon Name or National Pokédex Number: ', validators=[DataRequired()])
    submit_btn = SubmitField('Search')