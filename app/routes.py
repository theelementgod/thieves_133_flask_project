from flask import request, render_template
import requests
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/home')
def hello_trainer():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        return 'Successfully Logged In'
    else:
        return render_template('login.html' , form=form)

@app.route('/pkmn_name', methods=['GET', 'POST'])
def get_pkmn_data_name():
    if request.method == 'POST':
        pkmn_name = request.form.get('pkmn_name'.lower())
        pkmn_url = f'https://pokeapi.co/api/v2/pokemon/{pkmn_name}'
        pkmn_response = requests.get(pkmn_url)
        pkmn_data = pkmn_response.json()
        
        all_pkmn = get_pkmn_data(pkmn_data)
        return render_template('pkmn_name.html', all_pkmn=all_pkmn)
    else:
        return render_template('pkmn_name.html')

def get_pkmn_data(pkmn_data):
    new_pkmn_data =[]
    pkmn_dict = {
        'pkmn_name': (pkmn_data['forms'][0]['name']),
        'ability': pkmn_data['abilities'][0]['ability']['name'],
        'hp': pkmn_data['stats'][0]['base_stat'],
        'attack': pkmn_data['stats'][1]['base_stat'],
        'defense': pkmn_data['stats'][2]['base_stat'],
        'sp_attk': pkmn_data['stats'][3]['base_stat'],
        'sp_def': pkmn_data['stats'][4]['base_stat'],
        'speed': pkmn_data['stats'][5]['base_stat'],
        'shiny_sprite_url': pkmn_data['sprites']['front_shiny']
    }
    new_pkmn_data.append(pkmn_dict)
    return new_pkmn_data