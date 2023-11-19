from app.blueprints.pokemon import pokemon
from flask import render_template, request, flash, redirect, url_for
from flask_login import current_user
import requests
from .forms import PkmnForm
from app.models import Pokemon, db, User

@pokemon.route('/pkmn_name', methods=['GET', 'POST'])
def get_pkmn_data_name():
    if current_user.is_authenticated:
        user = User.query.get(current_user.id)
        team = user.catching
        all_pkmn = Pokemon.query.all()
        form = PkmnForm()
        if request.method == 'POST':
            pkmn_name = form.pkmn_name.data.lower()
            pokemonDuplicate = any(pkmn_name == pokemon.pkmn_name for pokemon in team)
            pokemonFound = any(pkmn_name == pokemon.name for pokemon in all_pkmn)
            if user.team.count() > 5:
                flash('You can no more than 6 Pokemon on your team.', 'danger')
                return render_template('pkmn_name.html', form=form)
            if pokemonDuplicate:
                flash('You already have { pkmnName } in your party.', 'warning')
                return render_template('pkmn_name.html', form=form)
            elif pokemonFound:
                pokemon = Pokemon.query.get(pkmn_name)
                user.team.append(pokemon)
                db.session.commit()
                return render_template('pkmn_name.html', form=form)
            else:
                pokemon_url=f"https://pokeapi.co/api/v2/pokemon/{pkmn_name}"
                pkmn_response = requests.get(pokemon_url)
                pkmn_data = pkmn_response.json()
                if pkmn_name:
                    pkmn_dict = {
                            'pkmn_name': pkmn_data['forms'][0]['name'],
                            'shiny_sprite_url': pkmn_data['sprites']['front_shiny'],
                            'ability': pkmn_data['abilities'][0]['ability']['name'],
                            'base_hp': pkmn_data['stats'][0]['base_stat'],
                            'attack': pkmn_data['stats'][1]['base_stat'],
                            'defense': pkmn_data['stats'][2]['base_stat'],
                            'sp_atk': pkmn_data['stats'][3]['base_stat'],
                            'sp_def': pkmn_data['stats'][4]['base_stat'],
                            'speed': pkmn_data['stats'][5]['base_stat']  
                    }
                    poke=Pokemon(pkmn_name=pkmn_dict['pkmn_name'], shiny_sprite_url=pkmn_dict['shiny_sprite_url'], 
                                ability=pkmn_dict['ability'], base_hp=pkmn_dict['base_hp'], attack=pkmn_dict['attack'], 
                                defense=pkmn_dict['defense'], sp_atk=pkmn_dict['sp_atk'], sp_def=pkmn_dict['sp_def'], speed=pkmn_dict['speed'])
                    db.session.add(poke)
                    db.session.commit()
                    flash(f'You have added { poke.pkmn_name } to your team!')
                    return render_template('pkmn_name.html', form=form)
                else:
                    return render_template('pkmn_name.html')
    else:
        return redirect(url_for('aut.login'))