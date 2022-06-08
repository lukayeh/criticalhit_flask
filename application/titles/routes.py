# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from application.titles import titles_blueprint
from flask import render_template
import utils # import utils!

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Render titles page                 #
###############################################
@titles_blueprint.route('/titles')
def titles():
    conn = utils.get_db_connection()
    titles = conn.execute('SELECT * FROM titles WHERE association = ?',str(my_company)).fetchall()
    roster = conn.execute("SELECT * FROM roster WHERE association LIKE '%'||?||'%' AND accolade IS NOT 'none'", [my_company]).fetchall()
    conn.close()
    return render_template('titles.html', title='Titles', titles=titles, roster=roster)
