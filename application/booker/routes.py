# app/booker/routes.py
# this is where you can put all your booker routes
from flask import render_template, request, redirect, flash, url_for
import post_runner # importing the runner
from application.booker import booker_blueprint
from flask import render_template
import utils # import utils!
from models import *
from sqlalchemy import or_, and_

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Define dict factory                #
###############################################
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

###############################################
#          Login required                     #
###############################################
from flask_login import login_required, current_user

@booker_blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

###############################################
#          Render Booker page                 #
###############################################
@booker_blueprint.route('/booker')
def booker():
    
    company = "%{}%".format(my_company)
    roster = Roster.query.filter(
                    Roster.association.like(company),
                    Roster.active=='active',
                    Roster.role=='wrestler').all()
    titles = Titles.query.all()
    return render_template('booker.html', title='Booker', roster=roster, titles=titles)

###############################################
#          Render booker_post page            #
###############################################
@booker_blueprint.route('/booker_post', methods=['POST'])
def booker_post():
    conn = utils.get_db_connection()

    participants_sql = Roster.query.filter(or_(
                                    Roster.id == request.form['participant1'],
                                    Roster.id == request.form['participant2'])).all()

    ## Update rating if they're in a fued!
    fueds = Fueds.query.filter(or_((and_(Fueds.participant_1==request.form['participant1'],Fueds.participant_2==request.form['participant2'])), \
              (and_(Fueds.participant_1==request.form['participant2'],Fueds.participant_2==request.form['participant1'])))).all()

    ## Grab titles
    titles = Titles.query.all()

    # set bonus to 0
    bonus = 0
    
    # Setup a titles list
    myTitles = []
    
    # Check for titles
    if 'titlematch' in request.form or 'titlematch_2' in request.form:
        print(f"titlematch set")

        # Append first title
        if "titlematch" in request.form:
            # Append first title
            myTitles.append(request.form['titlematch'])
        
        # Append second title
        if "titlematch_2" in request.form:
            # Append second title
            myTitles.append(request.form['titlematch_2'])
        
        # print(myTitles)
        joinedTitles = ",".join(myTitles)
        # print(joinedTitles)
        bonus = bonus +5
        flash(f"Title bonus added +5!") 
    else:
        print(f"titlematch NOT set")
        titlematch='false'
    
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

    # Check if the participants are in a fued if so give extra points!
    if fueds:
        print(f"They are in a fued together")
        bonus = bonus +10
        fued_bonus='true'
    else:
        fued_bonus='false'
        print(f"No fued found")
    
    booker = post_runner.booker(participants=participants_sql,bonuses=bonus,omgmoment=omgmoment,runin_moment=runin_moment)
    booker_string = ','.join(map(str, booker[1]))
    
    # conn.execute("INSERT INTO result (result, rating, description) VALUES (?, ?, ?)", [booker[2], booker[5], booker_string])
    
    # Add to the result table
    new_result = Result(
            result = booker[2],
            rating = booker[5],
            description = booker_string)
    db.session.add(new_result)
    # Update the loser
    update_loser = Roster.query.filter_by(name=booker[4]).first()
    update_loser.health = (update_loser.health) - 5
    update_loser.losses = update_loser.losses + 1
    # Update the winner
    update_winner = Roster.query.filter_by(name=booker[3]).first()
    update_winner.level = update_winner.level + 1
    update_winner.wins = update_winner.wins + 1
    
    # Update titles
    if 'titlematch' in request.form or 'titlematch_2' in request.form:
        update_loser.accolade = 'none'
        update_winner.accolade = joinedTitles
    
    db.session.commit()

    if fued_bonus == 'true':
        flash(f"Fued bonus added +10!") 
    return render_template('booker_post.html', 
            title='Booker',
			booker=booker,
            participants=participants_sql,
            myTitles=myTitles,
            titles=titles)