# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from application.results import results_blueprint
from flask import render_template
import utils # import utils!

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Render Results page                #
###############################################
@results_blueprint.route('/results')
def results():
    conn = utils.get_db_connection()
    results = conn.execute('SELECT * FROM result order by created desc limit 5').fetchall()
    conn.close()
    return render_template('results.html', title='Home', result=results)