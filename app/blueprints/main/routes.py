from . import main
from flask import render_template, request, flash, url_for, redirect
from app.models import Pokemon, db
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
    all_teams = Pokemon.query.all()
    return render_template('create_teams.html', all_teams=all_teams)