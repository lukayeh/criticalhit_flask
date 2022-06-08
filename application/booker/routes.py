# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
import post_runner # importing the runner
from application.booker import booker_blueprint
from flask import render_template
import utils # import utils!

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
#          Render Booker page                 #
###############################################
@booker_blueprint.route('/booker')
def booker():
	conn = utils.get_db_connection()
	roster = conn.execute("SELECT * FROM roster WHERE role = ? AND active = ? AND association LIKE '%'||?||'%'", ['wrestler','active',my_company]).fetchall()
	titles = conn.execute("SELECT * FROM titles").fetchall()

	conn.close()
	return render_template('booker.html', title='Booker', roster=roster, titles=titles)

###############################################
#          Render booker_post page            #
###############################################
@booker_blueprint.route('/booker_post', methods=['POST'])
def booker_post():
    conn = utils.get_db_connection()
    print("PRINT REQUEST FORM!!!!!")
    print(request.form)
    print(request)

    participants_sql = conn.execute('SELECT * FROM roster WHERE id = ? OR id = ?', (request.form['participant1'],request.form['participant2'])).fetchall()
    ## Update rating if they're in a fued!
    fueds = conn.execute('SELECT * FROM fueds WHERE (participant_1 = :participant_1 AND participant_2 = :participant_2) OR (participant_2 = :participant_1 AND participant_1 = :participant_2)', 
            {"participant_1": request.form['participant1'], "participant_2": request.form['participant2']})
    fueds = fueds.fetchall()

    ## Grab titles
    titles = conn.execute('SELECT * FROM titles').fetchall()
    # titles = titles.

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
    
    conn.execute("INSERT INTO result (result, rating, description) VALUES (?, ?, ?)", [booker[2], booker[5], booker_string])
	# Update the loser
    conn.execute("UPDATE roster SET health = health - 5 WHERE name = ?", [booker[4]])
    conn.execute("UPDATE roster SET losses = losses + 1 WHERE name = ?", [booker[4]])
	# Update the winner
    conn.execute("UPDATE roster SET level = level + 1 WHERE name = ?", [booker[3]])
    conn.execute("UPDATE roster SET wins = wins + 1 WHERE name = ?", [booker[3]])
    # Update Winner titles
    if 'titlematch' in request.form or 'titlematch_2' in request.form:
        conn.execute("UPDATE roster SET accolade = ? WHERE name = ?", [joinedTitles,booker[3]])
        conn.execute("UPDATE roster SET accolade = ? WHERE name = ?", ['none',booker[4]])
    # conn.execute('UPDATE roster SET accolade = TRIM(BOTH "," FROM REPLACE(REPLACE(accolade, ?, ''), ",,", ",")) WHERE name=?;', [myTitles[0],booker[4]])


    conn.commit()
    conn.close()
    if fued_bonus == 'true':
        flash(f"Fued bonus added +10!") 
    return render_template('booker_post.html', 
            title='Booker',
			booker=booker,
            participants=participants_sql,
            myTitles=myTitles,
            titles=titles)