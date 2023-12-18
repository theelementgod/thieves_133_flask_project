from . import main
from flask import render_template, request, flash, url_for, redirect, jsonify
from app.models import Pokemon, db, User, Battle
from .forms import CatchForm
from flask_login import current_user, login_required

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/team', methods=['GET', 'POST'])
@login_required
def team():
    form = CatchForm()
    if request.method == 'POST' and form.validate_on_submit():
        pkmn_name = form.pkmn_name.data.title()
        shiny_sprite_url = form.shiny_url.data
        ability = form.ability.data.title()
        base_hp = form.base_hp.data
        attack = form.attack.data
        defense = form.defense.data
        sp_atk = form.sp_atk.data
        sp_def = form.sp_def.data
        speed = form.speed.data
        trainer_id = current_user.id

        pokemon = Pokemon(pkmn_name, shiny_sprite_url, ability, base_hp,
                        attack, defense, sp_atk, sp_def, speed, trainer_id)

        db.session.add(pokemon)
        db.session.commit()

        flash(f'{pkmn_name} successfully added to Team!', 'success')
        return redirect(url_for('pokemon.pkmn_name'))
    else:
        return render_template('pkmn_name.html', form=form)
    
@main.route('/create_team')
@login_required
def catch():
    trainer = User.query.get(current_user.id)
    all_teams = trainer.catch
    return render_template('create_teams.html', all_teams=all_teams)

@main.route('/trainers')
@login_required
def show_trainers():
    all_trainers = User.query.all()
    return render_template('trainers.html', all_trainers=all_trainers)

@main.route('/battle')
@login_required
def battle():
    all_trainers = User.query.all()
    return render_template('battle.html', all_trainer=all_trainers)

@main.route('/battle/start', methods=['POST'])
@login_required
def start_battle():
    trainer1_id = request.json.get('trainer1_id')
    trainer2_id = request.json.get('trainer2_id')

    battle = Battle(trainer1_id=trainer1_id, trainer2_id=trainer2_id)
    db.session.add(battle)
    db.session.commit()

    return jsonify({'message': 'Begin Battle!', 'battle_id': battle.id})
                    
@main.route('/battle/turn/<int:battle_id>', methods=['POST'])
def next_turn(battle_id):
    battle = Battle.query.get_or_404(battle_id)
    battle.turn += 1

    trainer1_party = battle.trainer1.party.all()
    trainer2_party = battle.trainer2.party.all()
    for pokemon in trainer1_party + trainer2_party:
        pkmnhp = 0
        pkmnatk = 0
        pkmndef = 0
        pkmnspd = 0
        if Pokemon.attack > Pokemon.sp_atk:
            pkmnatk += Pokemon.attack
        else:
            pkmnatk += Pokemon.sp_atk
        if Pokemon.defense > Pokemon.sp_def:
            pkmndef += Pokemon.defense
        else:
            pkmndef += Pokemon.sp_def
        pkmnhp += Pokemon.base_hp
        pkmnspd += Pokemon.speed

        if trainer1_party.pkmnspd > trainer2_party.pkmnspd:
            faster = trainer1_party[pokemon]
            slower = trainer2_party[pokemon]
        else:
            faster = trainer2_party[pokemon]
            slower = trainer1_party[pokemon]
        
        if faster.attack > slower.defense:
            slower.pkmnhp -= (faster.attack - slower.defense)
        else:
            slower.pkmnhp -= 1

        if slower.attack > faster.defense:
            faster.pkmnhp -= (slower.attack - faster.defense)
        else:
            faster.pkmnhp -= 1
                
        pokemon.update_stats()

    db.session.commit()

    return jsonify({'message': 'Next turn...', 'turn': battle.turn})