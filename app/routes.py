from flask import request, render_template
import requests
from app import app
from app.forms import LoginForm, PkmnForm, Signupform


@app.route('/')
@app.route('/home')
def hello_trainer():
    return render_template('home.html')

REGISTERED_USER = {
    'jesse.delarosa@thieves.com': {
        'name': 'Jesse De La Rosa',
        'password': 'ilovegaming'
    }
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        if email in REGISTERED_USER and REGISTERED_USER[email]['password'] == password:
            return f'Hello, {REGISTERED_USER[email]["name"]}'
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = Signupform()
    if request.method == 'POST' and form.validate_on_submit():
        full_name = f'{form.first_name.data} {form.last_name.data}'
        email = form.email.data
        password = form.password.data

        REGISTERED_USER[email] ={
            'name': full_name,
            'password': password
        }

        return f'Thank you for signing up {full_name}!'
    else:
        return render_template('signup.html', form=form)
    

@app.route('/pkmn_name', methods=['GET', 'POST'])

def get_pkmn_data_name():
    form = PkmnForm()
    if request.method == 'POST':
        pkmn_name = form.pokemon.data
        try:
            pokemon_url=f"https://pokeapi.co/api/v2/pokemon/{pkmn_name}"
            pkmn_response = requests.get(pokemon_url)
            pkmn_data = pkmn_response.json()
            
            pkmn_dict = {
                    'pkmn_name': pkmn_data['forms'][0]['name'],
                    'ability': pkmn_data['abilities'][0]['ability']['name'],
                    'hp': pkmn_data['stats'][0]['base_stat'],
                    'attack': pkmn_data['stats'][1]['base_stat'],
                    'defense': pkmn_data['stats'][2]['base_stat'],
                    'sp_attk': pkmn_data['stats'][3]['base_stat'],
                    'sp_def': pkmn_data['stats'][4]['base_stat'],
                    'speed': pkmn_data['stats'][5]['base_stat'],
                    'shiny_sprite_url': pkmn_data['sprites']['front_shiny']
                }
           

            return render_template('pkmn_name.html', pkmntest=pkmn_dict, form=form)
        except:
            return render_template('pkmn_name.html', form=form)
    else:
        return render_template('pkmn_name.html', form=form)



