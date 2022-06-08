# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from application.indies import indies_blueprint
from flask import render_template
import utils # import utils!

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Render indies page                 #
###############################################
@indies_blueprint.route('/indies')
def indies():
    conn = utils.get_db_connection()
    roster = conn.execute("SELECT * FROM roster WHERE association = '0'").fetchall()
    conn.close()
    return render_template('indies.html', title='Indies', roster=roster)