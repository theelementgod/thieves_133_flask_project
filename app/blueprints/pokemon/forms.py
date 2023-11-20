from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, IntegerField
from wtforms.validators import DataRequired


class PkmnForm(FlaskForm):
    pkmn_name = StringField('Pokemon:', validators=[DataRequired()])
    submit_btn = SubmitField('Search')

class CatchForm(FlaskForm):
    pkmn_name = StringField('', validators=[DataRequired()])
    shiny_sprite_url = StringField('', validators=[DataRequired()])
    ability = StringField('Ability:', validators=[DataRequired()])
    base_hp = IntegerField('HP:', validators=[DataRequired()])
    attack = IntegerField('ATK:', validators=[DataRequired()])
    defense = IntegerField('DEF:', validators=[DataRequired()])
    sp_atk = IntegerField('SP.ATK:', validators=[DataRequired()])
    sp_def = IntegerField('SP.DEF:', validators=[DataRequired()])
    speed = IntegerField('SPD:', validators=[DataRequired()])
    trainer_id = IntegerField('Trainer ID:', validators=[DataRequired()])
    catch_btn = SubmitField('Catch!')
    release_btn = SubmitField('Release!')
    submit_btn = SubmitField('Search')