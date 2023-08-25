from flask import render_template, request, redirect, flash, url_for
from application.booker import match  # importing the runner
from application.booker import booker_blueprint
from flask import render_template
import utils  # import utils!
from models import *
from sqlalchemy import or_, and_
import random

###############################################
#          Module Level Variables             #
###############################################
my_company = 2

###############################################
#          Login required                     #
###############################################
from flask_login import login_required, current_user


@booker_blueprint.before_request
@login_required
def before_request():
    """Protect all of the admin endpoints."""
    pass



###############################################
#          Render Booker_multi page           #
###############################################
@booker_blueprint.route("/booker_multi", methods=["POST"])
def booker_multi():
    numberParticipants=request.form["participants"]
    company = "%{}%".format(my_company)
    roster = Roster.query.filter(
        Roster.association.like(company),
        Roster.active == "active",
        Roster.role == "wrestler",
    ).all()
    titles = Titles.query.all()
    return render_template(
        "booker_multi.html", title="Booker", roster=roster, numberParticipants=numberParticipants, titles=titles
    )


###############################################
#          Render Booker_multi page           #
###############################################
@booker_blueprint.route("/booker_multi_post", methods=["POST"])
def booker_multi_post():
    playerIds = []
    for x in request.form:
        playerIds.append(request.form[x])
    # playerIds = [1, 2, 3, 4]
    booker=match.Booker(playerIds)

    return render_template("booker_multi_post.html", booker=booker)