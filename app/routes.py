from flask import request, render_template, redirect, url_for, flash
import requests
from app import app
from app.forms import LoginForm, PkmnForm, SignupForm
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f'Hello, Trainer {queried_user.first_name}!', 'success')
            return redirect(url_for('home'))
        else:
            return 'Invalid email or password'
    else:
        return render_template('login.html', form=form)
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data

        user = User(first_name, last_name, email, password)

        db.session.add(user)
        db.session.commit()

        flash(f'Thank you for signing up Trainer {first_name}!', 'success')
        return redirect(url_for('login'))
    else:
        return render_template('signup.html', form=form)
    
@app.route('/logout')
@login_required
def logout():
    flash('Successfully logged out!', 'warning')
    logout_user()
    return redirect(url_for('home'))
    

@app.route('/pkmn_name', methods=['GET', 'POST'])
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
