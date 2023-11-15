from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

class Pokemon(db.Model):
    shiny_url = db.Column(db.String, nullable=False)
    pkmn_name = db.Column(db.String, primary_key=True)
    base_hp = db.Column(db.Integer, nullable=False)
    attack = db.Column(db.Integer, nullable=False)
    defense = db.Column(db.Integer, nullable=False)
    sp_atk = db.Column(db.Integer, nullable=False)
    sp_def = db.Column(db.Integer, nullable=False)
    speed = db.Column(db.Integer, nullable=False)

    def __init__(self, shiny_url, pkmn_name, base_hp, attack, defense, sp_atk, sp_def, speed):
        self.shiny_url = shiny_url
        self.pkmn_name = pkmn_name
        self.base_hp = base_hp
        self.attack = attack
        self.defense = defense
        self.sp_atk = sp_atk
        self.sp_def = sp_def
        self.speed = speed

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pokemon1 = db.Column(db.String, db.ForeignKey('pokemon.pkmn_name'), nullable=False)
    pokemon2 = db.Column(db.String, db.ForeignKey('pokemon.pkmn_name'), nullable=False)
    pokemon3 = db.Column(db.String, db.ForeignKey('pokemon.pkmn_name'), nullable=False)
    pokemon4 = db.Column(db.String, db.ForeignKey('pokemon.pkmn_name'), nullable=False)
    pokemon5 = db.Column(db.String, db.ForeignKey('pokemon.pkmn_name'), nullable=False)
    pokemon6 = db.Column(db.String, db.ForeignKey('pokemon.pkmn_name'), nullable=False)

    def __init__(self, pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6):
        self.pokemon1 = pokemon1
        self.pokemon2 = pokemon2
        self.pokemon3 = pokemon3
        self.pokemon4 = pokemon4
        self.pokemon5 = pokemon5
        self.pokemon6 = pokemon6