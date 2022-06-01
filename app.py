###############################################
#          Import some packages               #
###############################################
from flask import Flask, render_template, request, redirect, flash, url_for
from flask_bootstrap import Bootstrap5
import sqlite3
import post_runner # importing the runner
from collections import defaultdict

###############################################
#          Define dict factory                #
###############################################
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

###############################################
#          Define db connection               #
###############################################
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = dict_factory
    return conn

###############################################
#          Define flask app                   #
###############################################
app = Flask(__name__)
app.secret_key = "abc"  

###############################################
#          Disable caching                    #
###############################################

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

###############################################
#          Define Globals                     #
###############################################
@app.context_processor
def inject_globals():
    return dict(date="15/05/2022", region="NA")

###############################################
#          Module Level Variables             #
###############################################

my_company=2

###############################################
#          Render Home page                   #
###############################################
@app.route('/')
def home():
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM result order by created desc limit 5').fetchall()
    roster10 = conn.execute('SELECT * FROM roster order by level desc limit 5').fetchall()
    conn.close()
    return render_template('index.html', title='Home', result=results, roster10=roster10)

###############################################
#          Render Results page                #
###############################################
@app.route('/results')
def results():
    conn = get_db_connection()
    results = conn.execute('SELECT * FROM result order by created desc limit 5').fetchall()
    conn.close()
    return render_template('results.html', title='Home', result=results)

###############################################
#          Render Booker page                 #
###############################################
@app.route('/booker')
def booker():
	conn = get_db_connection()
	roster = conn.execute("SELECT * FROM roster WHERE role = ? AND active = ? AND association LIKE '%'||?||'%'", ['wrestler','active',my_company]).fetchall()
	conn.close()
	return render_template('booker.html', title='Booker', roster=roster)

###############################################
#          Render booker_post page            #
###############################################
@app.route('/booker_post', methods=['POST'])
def booker_post():
    conn = get_db_connection()
    print("PRINT REQUEST FORM!!!!!")
    print(request.form)
    participants_sql = conn.execute('SELECT * FROM roster WHERE id = ? OR id = ?', (request.form['participant1'],request.form['participant2'])).fetchall()
    ## Update rating if they're in a fued!
    fueds = conn.execute('SELECT * FROM fueds WHERE (participant_1 = :participant_1 AND participant_2 = :participant_2) OR (participant_2 = :participant_1 AND participant_1 = :participant_2)', 
            {"participant_1": request.form['participant1'], "participant_2": request.form['participant2']})
    fueds = fueds.fetchall()
    # set bonus to 0
    bonus = 0
    
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

    conn.commit()
    conn.close()
    if fued_bonus == 'true':
        flash(f"Fued bonus added +10!") 
    return render_template('booker_post.html', 
            title='Booker',
			booker=booker,
            participants=participants_sql)

###############################################
#          Render Show Booker page            #
###############################################
@app.route('/show_booker')
def show_booker():
	conn = get_db_connection()
	roster = conn.execute("SELECT * FROM roster WHERE role = ? AND active = ? AND association LIKE '%'||?||'%'", ['wrestler','active',my_company]).fetchall()
	conn.close()
	return render_template('show_booker.html', title='Booker', roster=roster)

###############################################
#          Render show_post page              #
###############################################
@app.route('/show_post')
def show_post():
    show = {}
    no_segments = 5
    for x in range(1, no_segments):
        show[f'segment_{x}'] = {}
        show[f'segment_{x}']['participant_1'] = f"{request.args[f'0{x}_participant1']}"
        show[f'segment_{x}']['participant_2'] = f"{request.args[f'0{x}_participant2']}"
    conn = get_db_connection()
    roster = conn.execute('SELECT * FROM roster').fetchall()
    
    myResults = []

    for x in show.items():
        
        b = roster[int(x[1]['participant_1']) -1]
        c = roster[int(x[1]['participant_2']) -1]  
        myList = []
        myList.append(b)
        myList.append(c)
        booker = post_runner.booker(participants=myList)
        myResults.append(booker)

    return render_template('show_results.html', title='show_results', myResults=myResults)

    # return str(roster)

###############################################
#          Render member page                 #
###############################################
@app.route('/member')
def member():
    conn = get_db_connection()
    member = conn.execute('SELECT * FROM roster WHERE id = (?)', [request.args['member_id']]).fetchall()
    titles = conn.execute('SELECT * FROM titles').fetchall()
    associations = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return render_template('member.html', title='Member', member=member, titles=titles, companies=associations)


# Hire Worker
@app.route('/hire_member/', methods=('GET', 'POST'))
def hire_member():
    if request.method == 'POST':
        worker_to_hire = request.form['worker_to_hire']
        worker_name = request.form['worker_name']
        print(worker_to_hire)
        if not worker_to_hire:
            flash('worker_to_hire is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE roster SET association = ? WHERE id = (?)',
                             [my_company,worker_to_hire])
        #      conn.execute("UPDATE roster SET health = health - 5 WHERE name = ?", [booker[4]])

            conn.commit()
            conn.close()
            flash(f"you are successfuly hired {worker_name}")  
            return redirect(url_for('roster'))

@app.route('/fire_member/', methods=('GET', 'POST'))
def fire_member():
    if request.method == 'POST':
        worker_to_fire = request.form['worker_to_fire']
        worker_name = request.form['worker_name']
        print(worker_to_fire)
        if not worker_to_fire:
            flash('worker_to_fire is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE roster SET association = ? WHERE id = (?)',
                             [0,worker_to_fire])
        #      conn.execute("UPDATE roster SET health = health - 5 WHERE name = ?", [booker[4]])

            conn.commit()
            conn.close()
            flash(f"you are successfuly fired {worker_name}")  
            return redirect(url_for('roster'))

###############################################
#          Render roster page                 #
###############################################
@app.route('/roster')
def roster():
    conn = get_db_connection()
    roster = conn.execute("SELECT * FROM roster WHERE association LIKE '%'||?||'%'", str(my_company)).fetchall()
    titles = conn.execute('SELECT * FROM titles').fetchall()
    conn.close()
    return render_template('roster.html', title='Roster', roster=roster, titles=titles)

###############################################
#          Render fued page                   #
###############################################

@app.route('/fueds')
def fueds():
    conn = get_db_connection()
    roster = conn.execute("SELECT * FROM roster").fetchall()
    fueds = conn.execute("SELECT * FROM fueds WHERE company = ?", [my_company]).fetchall()
    conn.close()
    return render_template('fueds.html', title='Fueds', roster=roster, fueds=fueds)


@app.route('/create_fued/', methods=('GET', 'POST'))
def create_fued():
    conn = get_db_connection()
    roster = conn.execute("SELECT * FROM roster WHERE role = ? AND active = ? AND association LIKE '%'||?||'%'", ['wrestler','active',my_company]).fetchall()
    conn.close()

    if request.method == 'POST':
        participant_1 = request.form['participant1']
        participant_2 = request.form['participant2']

        if not participant_1:
            flash('Title is required!')
        elif not participant_2:
            flash('Content is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO fueds (participant_1, participant_2, popularity, status, company) VALUES (?, ?, ?, ?, ?)',
                            (participant_1, participant_2,0,"active",my_company))
            conn.commit()
            conn.close()
            flash(f"you have successfuly created a fued")  
            return redirect(url_for('fueds'))
    return render_template('create.html',roster=roster)

@app.route('/delete_fued/', methods=('GET', 'POST'))
def delete_fued():
    if request.method == 'POST':
        fued_to_delete = request.form['fued_to_delete']
        print(fued_to_delete)
        if not fued_to_delete:
            flash('fued_to_delete is required!')
        else:
            conn = get_db_connection()
            # conn.execute('DELETE FROM fueds WHERE id = (?)',
            #                 [fued_to_delete])
            conn.execute('UPDATE fueds SET status = ? WHERE id = (?)',
                             ['ended',fued_to_delete])
        #      conn.execute("UPDATE roster SET health = health - 5 WHERE name = ?", [booker[4]])

            conn.commit()
            conn.close()
            flash(f"you have successfuly ended the fued")  
            return redirect(url_for('fueds'))
    # return render_template('create.html',roster=roster)

###############################################
#          Render indies page                 #
###############################################
@app.route('/indies')
def indies():
    conn = get_db_connection()
    roster = conn.execute("SELECT * FROM roster WHERE association = '0'").fetchall()
    conn.close()
    return render_template('indies.html', title='Indies', roster=roster)


###############################################
#          Render companies page              #
###############################################
@app.route('/companies')
def companies():
    conn = get_db_connection()
    companies = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return render_template('companies.html', title='Companies', companies=companies)

###############################################
#          Render titles page                 #
###############################################
@app.route('/titles')
def titles():
    conn = get_db_connection()
    titles = conn.execute('SELECT * FROM titles WHERE association = ?',str(my_company)).fetchall()
    roster = conn.execute("SELECT * FROM roster WHERE association LIKE '%'||?||'%' AND accolade IS NOT 'none'", [my_company]).fetchall()
    conn.close()
    return render_template('titles.html', title='Titles', titles=titles, roster=roster)




###############################################
#             Init our app                    #
###############################################
# nav.init_app(app)
bootstrap = Bootstrap5(app)


###############################################
#                Run app                      #
###############################################
if __name__ == '__main__':
    app.run(debug=True,threaded=True)