# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Blueprint
from flask import Flask, render_template, request, redirect, flash, url_for
import sqlite3
from application.indies import indies_blueprint
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

@indies_blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

###############################################
#          Render indies page                 #
###############################################
@indies_blueprint.route('/indies')
def indies():
    
    roster = Roster.query.filter(Roster.association.like('0')).all()

    return render_template('indies.html', title='Indies', roster=roster)