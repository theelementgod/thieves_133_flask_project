from . import team
from flask import request, flash, url_for, redirect, render_template
from app.models import Team, db
from .forms import TeamForm
from flask_login import login_required

@team.route('/create_team', methods=['GET', 'POST'])
@login_required
def create_team():
    form = TeamForm()
    if request.method == 'POST' and form.validate_on_submit():
        pokemon1 = form.pokemon1.data
        pokemon2 = form.pokemon2.data
        pokemon3 = form.pokemon3.data
        pokemon4 = form.pokemon4.data
        pokemon5 = form.pokemon5.data
        pokemon6 = form.pokemon6.data

        team = Team(pokemon1, pokemon2, pokemon3, pokemon4, pokemon5, pokemon6)

        db.session.add(team)
        db.session.commit()

        flash(f'Pokemon added to the Team!', 'success')
        return redirect(url_for('team.roster'))
    else:
        return render_template('create_team.html', form=form)