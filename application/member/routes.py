# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from application.member import member_blueprint
from flask import render_template
import utils # import utils!

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Render member page                 #
###############################################
@member_blueprint.route('/member')
def member():
    conn = utils.get_db_connection()
    member = conn.execute('SELECT * FROM roster WHERE id = (?)', [request.args['member_id']]).fetchall()
    titles = conn.execute('SELECT * FROM titles').fetchall()
    associations = conn.execute('SELECT * FROM companies').fetchall()
    conn.close()
    return render_template('member.html', title='Member', member=member, titles=titles, companies=associations)


# Hire Worker
@member_blueprint.route('/hire_member/', methods=('GET', 'POST'))
def hire_member():
    if request.method == 'POST':
        worker_to_hire = request.form['worker_to_hire']
        worker_name = request.form['worker_name']
        print(worker_to_hire)
        if not worker_to_hire:
            flash('worker_to_hire is required!')
        else:
            conn = utils.get_db_connection()
            conn.execute('UPDATE roster SET association = ? WHERE id = (?)',
                             [my_company,worker_to_hire])
        #      conn.execute("UPDATE roster SET health = health - 5 WHERE name = ?", [booker[4]])

            conn.commit()
            conn.close()
            flash(f"you are successfuly hired {worker_name}")  
            return redirect(url_for('roster_assets.roster'))

@member_blueprint.route('/fire_member/', methods=('GET', 'POST'))
def fire_member():
    if request.method == 'POST':
        worker_to_fire = request.form['worker_to_fire']
        worker_name = request.form['worker_name']
        print(worker_to_fire)
        if not worker_to_fire:
            flash('worker_to_fire is required!')
        else:
            conn = utils.get_db_connection()
            conn.execute('UPDATE roster SET association = ? WHERE id = (?)',
                             [0,worker_to_fire])
        #      conn.execute("UPDATE roster SET health = health - 5 WHERE name = ?", [booker[4]])

            conn.commit()
            conn.close()
            flash(f"you are successfuly fired {worker_name}")  
            return redirect(url_for('roster_assets.roster'))

@member_blueprint.route('/edit_member/', methods=('GET', 'POST'))
def edit_member():
    worker_to_edit = request.args['member_id']
    conn = utils.get_db_connection()
    member = conn.execute('SELECT * FROM roster WHERE id = (?)', [worker_to_edit]).fetchall()
    print(worker_to_edit)
    conn.close()
        
    return render_template('member_edit.html',
                            member=member)

@member_blueprint.route('/submit_member/', methods=('GET', 'POST'))
def submit_member():
    # print(request.method)
    if request.method == 'POST':
        print("PRINT REQUEST FORM!!!!!")
        print(request.form)
        conn = utils.get_db_connection()
        # conn.execute("UPDATE roster SET accolade = ? WHERE id = ?", 
        conn.execute("""UPDATE roster
            SET name = ?,
                real_name = ?,
                role = ?,
                association = ?,
                accolade = ?,
                active = ?,
                finisher = ?,
                attack = ?,
                defense = ?,
                health = ?,
                level = ?,
                wins = ?,
                losses = ?,
                img = ?
            WHERE id = ?""",
            [ request.form['name'],
                request.form['realName'],
                request.form['role'],
                request.form['association'],
                request.form['accolade'],
                request.form['active'],
                request.form['finisher'],
                request.form['attack'],
                request.form['defense'],
                request.form['health'],
                request.form['level'],
                request.form['wins'],
                request.form['losses'],
                request.form['img'],
                request.form['id'] ])

        conn.commit()
        conn.close()

        flash(f"you have successfuly updated member")  
    return redirect(url_for('roster_assets.roster'))
