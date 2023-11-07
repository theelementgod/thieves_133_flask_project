from flask import Flask, request, render_template
import requests

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def hello_trainer():
    return'<h1>Welcome Trainer!</h1>'

@app.route('/pkmn_name', methods=['GET', 'POST'])
def get_pkmn_data_name():
    if request.method == 'POST':
        pkmn_name = request.form.get('pkmn_name')
        pkmn_url = f'https://pokeapi.co/api/v2/pokemon/{pkmn_name}'
        pkmn_response = requests.get(pkmn_url)
        pkmn_data = pkmn_response.json()
        return render_template('pkmn_name.html', pkmn_data=pkmn_data)
    else:
        return render_template('pkmn_name.html')

def get_pkmn_data(pkmn_data):
    new_pkmn_data =[]
    for pkmn in pkmn_data:
        pkmn_dict = {
            'shiny_sprite_url': pkmn['sprites']['front_shiny'],
            'pkmn_name': pkmn['forms'][0]['name'],
            'ability': pkmn['abilities'][0]['ability']['name'],
            'hp': pkmn['stats'][0]['base_stat'],
            'attack': pkmn['stats'][1]['base_stat'],
            'defense': pkmn['stats'][2]['base_stat']
        }
        new_pkmn_data.append(pkmn_dict)
    return new_pkmn_data




# @app.route('/f1/driverStandings', methods=['GET', 'POST'])
# def get_driver_data_year_rnd():

#     if request.method == 'POST':
#         year = request.form.get('year')
#         rnd = request.form.get('rnd')
#         url = f'https://ergast.com/api/f1/{year}/{rnd}/driverStandings.json'
#         response = requests.get(url)
#         try:
#             new_data = response.json()['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
#             # call helper function
#             all_drivers = get_driver_data(new_data)
#             return render_template('driverStandings.html', all_drivers=all_drivers)
#         except IndexError:
#             return 'Invalid round or year'
#     else:
#         return render_template('driverStandings.html')

# def get_driver_data(data):
#     new_driver_data = []
#     for driver in data:
#         driver_dict = {
#             'first_name': driver['Driver']['givenName'],
#             'last_name': driver['Driver']['familyName'],
#             'DOB': driver['Driver']['dateOfBirth'],
#             'wins': driver['wins'],
#             'team': driver['Constructors'][0]['name']
#         }
#         new_driver_data.append(driver_dict)
#     return new_driver_data
