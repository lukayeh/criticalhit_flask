# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
import post_runner # importing the runner
from application.show_booker import show_booker_blueprint
from flask import render_template
import utils # import utils!

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Render Show Booker page            #
###############################################
@show_booker_blueprint.route('/show_booker')
def show_booker():
	conn = utils.get_db_connection()
	roster = conn.execute("SELECT * FROM roster WHERE role = ? AND active = ? AND association LIKE '%'||?||'%'", ['wrestler','active',my_company]).fetchall()
	conn.close()
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
    conn = utils.get_db_connection()
    roster = conn.execute('SELECT * FROM roster').fetchall()
    conn.close()
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