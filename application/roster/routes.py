# app/booker/routes.py
# this is where you can put all your booker routes
from flask import render_template, request, redirect, flash, url_for
from application.roster import roster_blueprint
from flask import render_template
from models import *

###############################################
#          Module Level Variables             #
###############################################
my_company = 2


###############################################
#          Login required                     #
###############################################
from flask_login import login_required, current_user


@roster_blueprint.before_request
@login_required
def before_request():
    """Protect all of the admin endpoints."""
    pass


###############################################
#          Render roster page                 #
###############################################
@roster_blueprint.route("/roster")
def roster():
    search = "%{}%".format(my_company)
    roster = Roster.query.filter(Roster.association.like(search)).all()

    titles = Titles.query.all()
    return render_template("roster_test.html", roster=roster, titles=titles)
