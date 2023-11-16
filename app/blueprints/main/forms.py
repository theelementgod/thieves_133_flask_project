from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired



class PkmnForm(FlaskForm):
    pkmn_name = StringField('Pokemon: ', validators=[DataRequired()])
    shiny_sprite_url = StringField('Image: ', validators=[DataRequired()])
    ability_name = StringField('Ability: ', validators=[DataRequired()])
    base_hp = IntegerField('Base HP: ', validators=[DataRequired()])
    attack_stat = IntegerField('ATK: ', validators=[DataRequired()])
    defense_stat = IntegerField('DEF: ', validators=[DataRequired()])
    spatk_stat = IntegerField('SP.ATK: ', validators=[DataRequired()])
    spdef_stat = IntegerField('SP.DEF: ', validators=[DataRequired()])
    speed_stat = IntegerField('SPD: ', validators=[DataRequired()])
    submit_btn = SubmitField('Submit')