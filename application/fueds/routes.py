# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from application.fueds import fueds_blueprint
from flask import render_template
import utils # import utils!

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Render fued page                   #
###############################################

@fueds_blueprint.route('/fueds')
def fueds():
    conn = utils.get_db_connection()
    roster = conn.execute("SELECT * FROM roster").fetchall()
    fueds = conn.execute("SELECT * FROM fueds WHERE company = ?", [my_company]).fetchall()
    conn.close()
    return render_template('fueds.html', title='Fueds', roster=roster, fueds=fueds)


@fueds_blueprint.route('/create_fued/', methods=('GET', 'POST'))
def create_fued():
    conn = utils.get_db_connection()
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
            conn = utils.get_db_connection()
            conn.execute('INSERT INTO fueds (participant_1, participant_2, popularity, status, company) VALUES (?, ?, ?, ?, ?)',
                            (participant_1, participant_2,0,"active",my_company))
            conn.commit()
            conn.close()
            flash(f"you have successfuly created a fued")  
            return redirect(url_for('fueds_assets.fueds'))
    return render_template('fued_create.html',roster=roster)

@fueds_blueprint.route('/delete_fued/', methods=('GET', 'POST'))
def delete_fued():
    if request.method == 'POST':
        fued_to_delete = request.form['fued_to_delete']
        print(fued_to_delete)
        if not fued_to_delete:
            flash('fued_to_delete is required!')
        else:
            conn = utils.get_db_connection()
            conn.execute('UPDATE fueds SET status = ? WHERE id = (?)',
                             ['ended',fued_to_delete])

            conn.commit()
            conn.close()
            flash(f"you have successfuly ended the fued")  
            return redirect(url_for('fueds_assets.fueds'))
