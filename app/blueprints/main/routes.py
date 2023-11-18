from . import main
from flask import render_template

@main.route('/')
@main.route('/home')
def home():
    return render_template('home.html')

