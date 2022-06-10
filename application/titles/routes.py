# app/booker/routes.py
# this is where you can put all your booker routes
from flask import render_template, request, redirect, flash, url_for
from application.titles import titles_blueprint
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

@titles_blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

###############################################
#          Render titles page                 #
###############################################
@titles_blueprint.route('/titles')
def titles():
    search = "%{}%".format(my_company)
    roster = Roster.query.filter(Roster.association.like(search)).all()
    titles = Titles.query.filter(Titles.association.like(search)).all()

    return render_template('titles.html', title='Titles', titles=titles, roster=roster)
