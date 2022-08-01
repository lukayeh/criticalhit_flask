# app/booker/routes.py
# this is where you can put all your booker routes
from flask import render_template, request, redirect, flash, url_for
from application.results import results_blueprint
from flask import render_template
import utils  # import utils!
from models import *

###############################################
#          Module Level Variables             #
###############################################
my_company = 2


###############################################
#          Login required                     #
###############################################
from flask_login import login_required, current_user


@results_blueprint.before_request
@login_required
def before_request():
    """Protect all of the admin endpoints."""
    pass


###############################################
#          Render Results page                #
###############################################
@results_blueprint.route("/results")
def results():
    results = Result.query.filter().all()
    return render_template("results.html", title="Home", result=results)
