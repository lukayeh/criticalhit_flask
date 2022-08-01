# app/booker/routes.py
# this is where you can put all your booker routes
from flask import render_template, request, redirect, flash, url_for
from application.home import home_blueprint
from flask import render_template
from models import *
from flask_login import login_required, current_user

###############################################
#          Module Level Variables             #
###############################################
my_company = 2

###############################################
#          Login required                     #
###############################################
from flask_login import login_required, current_user


@home_blueprint.before_request
@login_required
def before_request():
    """Protect all of the admin endpoints."""
    pass


###############################################
#          Render Home page                   #
###############################################
@home_blueprint.route("/")
def home():

    roster10 = Roster.query.order_by(Roster.level.desc()).limit(5).all()
    results = Result.query.order_by(Result.rating.desc()).limit(5).all()

    return render_template(
        "index.html",
        title="Home",
        result=results,
        roster10=roster10,
        name=current_user.name,
    )


@home_blueprint.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)
