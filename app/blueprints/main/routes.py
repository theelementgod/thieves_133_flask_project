from app.blueprints.main import main
from flask import render_template, request, flash, url_for, redirect
from flask_login import login_required
import requests
from app.models import db, Pokemon
from .forms import PkmnForm

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/pkmn_name', methods=['GET', 'POST'])
@login_required
def get_pkmn_data_name():
    form = PkmnForm()
    if request.method == 'POST' and form.validate_on_submit():
        pkmn_name = form.pkmn_name.data.lower()
        shiny_sprite_url = form.shiny_sprite_url.data.lower()
        ability_name = form.ability_name.data.lower()
        base_hp = form.base_hp.data.lower()
        attack_stat = form.attack_stat.data.lower()
        defense_stat = form.defense_stat.data.lower()
        spatk_stat = form.spatk_stat.data.lower()
        spdef_stat = form.spdef_stat.data.lower()
        spd_stat = form.speed_stat.data.lower()

        pokemon = Pokemon(pkmn_name, shiny_sprite_url, ability_name, base_hp, attack_stat, defense_stat, spatk_stat, spdef_stat, spd_stat)

        if pokemon:
            return render_template('pkmn_name.html', pokemon=pokemon, form=form)
        else:
            pokemon_url=f"https://pokeapi.co/api/v2/pokemon/{pkmn_name}"
            pkmn_response = requests.get(pokemon_url)
            pkmn_data = pkmn_response.json()
            pkmn_dict = {
                    'shiny_sprite_url': pkmn_data['sprites']['front_shiny'],
                    'pkmn_name': pkmn_data['forms'][0]['name'],
                    'ability': pkmn_data['abilities'][0]['ability']['name'],
                    'base_hp': pkmn_data['stats'][0]['base_stat'],
                    'attack': pkmn_data['stats'][1]['base_stat'],
                    'defense': pkmn_data['stats'][2]['base_stat'],
                    'sp_attk': pkmn_data['stats'][3]['base_stat'],
                    'sp_def': pkmn_data['stats'][4]['base_stat'],
                    'speed': pkmn_data['stats'][5]['base_stat']  
                }
            poke=Pokemon(shiny_sprite=pkmn_dict['shiny_sprite_url'], pokemon_name=pkmn_dict['pkmn_name'], ability_name=pkmn_dict['ability'], base_hp=pkmn_dict['base_hp'], 
                         attack_stat=pkmn_dict['attack'], defense_stat=pkmn_dict['defense'], spattk_stat=pkmn_dict['sp_attk'], spdef_stat=pkmn_dict['sp_def'], speed_stat=pkmn_dict['speed'])


        
        db.session.add(pokemon)
        db.session.commit()

        flash(f'Way to go, {{ current_user.id }}!  You caught a {{ pokemon.pkmn_name }} and added it to your team!', 'success')
        return redirect(url_for('main.pkmn_name'))
    else:
        return render_template('create_roster.html', form=form)
    