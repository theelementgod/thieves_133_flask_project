from app.blueprints.pokemon import pokemon
from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
import requests
from .forms import PkmnForm
from app.models import Pokemon, db, User

@pokemon.route('/pkmn_name', methods=['GET', 'POST'])
@login_required
def get_pkmn_data_name():
    form = PkmnForm()
    if request.method == 'POST' and form.validate_on_submit():
        pkmn_name = form.pkmn_name.data.lower()
        poke = Pokemon.query.get(pkmn_name)
        if poke:
            return render_template('pkmn_name.html', poke=poke, form=form)
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
                return render_template('pkmn_name.html', poke=poke, form=form)
            except:
                return render_template('pkmn_name.html', form=form)
    else:
        return render_template('pkmn_name.html', form=form)
    
@pokemon.route('/catch/<string:pkmn_name>',methods=['GET'])
@login_required
def catch(pkmn_name):
    print(pkmn_name)
    pokemon = Pokemon.query.get(pkmn_name)
    current_user.catch.append(pokemon)
    db.session.commit()
    flash(f'You have added { pkmn_name } to your team!', 'success')
    return redirect(url_for('pokemon.get_pkmn_data_name'))
    
@pokemon.route('/team')
def team():
    all_pkmn = Pokemon.query.filter(User.id == current_user.id).all()
    print(all_pkmn)
    return render_template('team.html', all_pkmn=all_pkmn)