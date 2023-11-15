from app.blueprints.main import main
from flask import render_template, request
from flask_login import login_required
import requests
from app.blueprints.main.forms import PkmnForm

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

@main.route('/pkmn_name', methods=['GET', 'POST'])
@login_required
def get_pkmn_data_name():
    form = PkmnForm()
    if request.method == 'POST' and form.validate_on_submit():
        pkmn_name = form.pokemon.data.lower()
        try:
            pokemon_url=f"https://pokeapi.co/api/v2/pokemon/{pkmn_name}"
            pkmn_response = requests.get(pokemon_url)
            pkmn_data = pkmn_response.json()
            pkmn_dict = {
                    'shiny_sprite_url': pkmn_data['sprites']['front_shiny'],
                    'pkmn_name': pkmn_data['forms'][0]['name'],
                    'ability': pkmn_data['abilities'][0]['ability']['name'],
                    'hp': pkmn_data['stats'][0]['base_stat'],
                    'attack': pkmn_data['stats'][1]['base_stat'],
                    'defense': pkmn_data['stats'][2]['base_stat'],
                    'sp_attk': pkmn_data['stats'][3]['base_stat'],
                    'sp_def': pkmn_data['stats'][4]['base_stat'],
                    'speed': pkmn_data['stats'][5]['base_stat']  
                }
            return render_template('pkmn_name.html', pkmn_name=pkmn_dict, form=form)
        except:
            return render_template('pkmn_name.html', form=form)
    else:
        return render_template('pkmn_name.html', form=form)