# app/booker/routes.py
# this is where you can put all your booker routes
from flask import render_template, request, redirect, flash, url_for
from application.booker import post_runner # importing the runner
from application.show_booker import show_booker_blueprint
from flask import render_template
import utils # import utils!
from models import * 

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Login required                     #
###############################################
from flask_login import login_required, current_user

@show_booker_blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

###############################################
#          Render Show Booker page            #
###############################################
@show_booker_blueprint.route('/show_booker')
def show_booker():
    company = "%{}%".format(my_company)
    roster = Roster.query.filter(
                    Roster.association.like(company),
                    Roster.active=='active',
                    Roster.role=='wrestler').all()
    # titles = Titles.query.all()
    return render_template('show_booker.html', title='Booker', roster=roster)

###############################################
#          Render show_post page              #
###############################################
@show_booker_blueprint.route('/show_post')
def show_post():
    show = {}
    no_segments = 5
    for x in range(1, no_segments):
        show[f'segment_{x}'] = {}
        show[f'segment_{x}']['participant_1'] = f"{request.args[f'0{x}_participant1']}"
        show[f'segment_{x}']['participant_2'] = f"{request.args[f'0{x}_participant2']}"
    roster = Roster.query.all()
    myResults = []

    for x in show.items():
        
        b = roster[int(x[1]['participant_1']) -1]
        c = roster[int(x[1]['participant_2']) -1]  
        myList = []
        myList.append(b)
        myList.append(c)
        
        bonus=0

        # Check for omg moment
        if 'omgmoment' in request.form:
            print(f"OMG moment set")
            omgmoment='true'
            bonus = bonus +5
        else:
            print(f"OMG moment NOT set")
            omgmoment='false'

        # Check for run in moment
        if 'run_in' in request.form:
            print(f"Random run_in moment set")
            runin_moment='true'
            bonus = bonus +5
        else:
            print(f"Random run_in moment NOT set")
            runin_moment='false'

        booker = post_runner.booker(participants=myList,bonuses=bonus,omgmoment=omgmoment,runin_moment=runin_moment)
        myResults.append(booker)

    return render_template('show_results.html', title='show_results', myResults=myResults)

    # return str(roster)