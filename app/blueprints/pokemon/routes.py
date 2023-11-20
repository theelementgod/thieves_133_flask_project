from app.blueprints.pokemon import pokemon
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from .forms import PkmnForm, CatchForm
from app.models import Pokemon, db

@pokemon.route('/pkmn_name', methods=['GET', 'POST'])
@login_required
def get_pkmn_data_name():
    form = PkmnForm()
    if request.method == 'POST' and form.validate_on_submit():
        pkmn_name = form.pkmn_name.data.lower()
        poke = Pokemon.query.get(pkmn_name)
        if poke:
            return render_template('pkmn_html', poke=poke)
        else:
            pkmn_name = form.pkmn_name.data.lower()
            try:
                pokemon_url=f"https://pokeapi.co/api/v2/pokemon/{pkmn_name}"
                pkmn_response = requests.get(pokemon_url)
                pkmn_data = pkmn_response.json()
                pkmn_dict = {
                        'pkmn_name': pkmn_data['forms'][0]['name'],
                        'shiny_sprite_url': pkmn_data['sprites']['front_shiny'],
                        'ability': pkmn_data['abilities'][0]['ability']['name'],
                        'base_hp': pkmn_data['stats'][0]['base_stat'],
                        'attack': pkmn_data['stats'][1]['base_stat'],
                        'defense': pkmn_data['stats'][2]['base_stat'],
                        'sp_attk': pkmn_data['stats'][3]['base_stat'],
                        'sp_def': pkmn_data['stats'][4]['base_stat'],
                        'speed': pkmn_data['stats'][5]['base_stat']  
                    }
                poke = Pokemon(pkmn_name=pkmn_dict['pkmn_name'], shiny_sprite_url=pkmn_dict['shiny_sprite_url'], ability=pkmn_dict['ability'], base_hp=pkmn_dict['base_hp'],
                               attack=pkmn_dict['attack'], defense=pkmn_dict['defense'], sp_atk=pkmn_dict['sp_attk'], sp_def=pkmn_dict['sp_def'], speed=pkmn_dict['speed'])
                db.session.add(poke)
                db.session.commit()
                return render_template('pkmn_name.html', poke=poke)
            except:
                return render_template('pkmn_name.html', form=form)
    else:
        return render_template('pkmn_name.html', form=form)
    
@pokemon.route('/catch/<int:pkmn_name>',methods=['GET'])
@login_required
def catch(pkmn_name):
    form = CatchForm()
    if request.method == 'GET':
        pokemon = Pokemon.query.get(pkmn_name)
        if pokemon:
            current_user.team.append(pokemon)
        else:

            pkmn_name = form.pkmn_name.data.lower()
            shiny_sprite_url = form.shiny_sprite_url.data
            ability = form.ability.data
            base_hp = form.base_hp.data
            attack = form.attack.data
            defense = form.defense.data
            sp_atk = form.sp_atk.data
            sp_def = form.sp_def.data
            speed = form.speed.data
            trainer_id = current_user.id

            pokemon = Pokemon(pkmn_name, shiny_sprite_url, ability, base_hp, attack, defense, sp_atk, sp_def, speed, trainer_id)

            db.session.add(pokemon)
            db.session.commit()
            current_user.team.append(pokemon)

            flash(f'You have added { pkmn_name } to your team!', 'success')
            return redirect(url_for('pokemon.pkmn_name'))
    else:
        return render_template('pkmn_name.html', form=form)
    
@pokemon.route('/team')
def team():
    all_pkmn = Pokemon.query.all()
    print(all_pkmn)
    return render_template('team.html', all_pkmn=all_pkmn)