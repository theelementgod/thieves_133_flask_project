from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

user_pokemon = db.Table('user_pokemon',
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('pokemon_name', db.String, db.ForeignKey('pokemon.pkmn_name'))
)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    catching = db.relationship('Pokemon', secondary=user_pokemon, backref='caught')

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

class Pokemon(db.Model):
    pkmn_name = db.Column(db.String, primary_key=True)
    shiny_sprite_url = db.Column(db.String, nullable=False)
    ability = db.Column(db.String, nullable=False)
    base_hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    sp_atk = db.Column(db.Integer, nullable=False)
    sp_def = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, pkmn_name, shiny_sprite_url, ability, base_hp, attack, defense, sp_atk, sp_def, speed, trainer_id):
        self.pkmn_name = pkmn_name
        self.shiny_sprite_url = shiny_sprite_url
        self.ability = ability
        self.base_hp = base_hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed
        self.trainer_id = trainer_id