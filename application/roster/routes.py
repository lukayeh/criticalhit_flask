# app/booker/routes.py
# this is where you can put all your booker routes
from flask import Flask, render_template, request, redirect, flash, url_for
from application.roster import roster_blueprint
from flask import render_template
import utils # import utils!
from app import app
from models import Roster, Titles

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Render roster page                 #
###############################################
@roster_blueprint.route('/roster')
def roster():
    search = "%{}%".format(my_company)
    roster = Roster.query.filter(Roster.association.like(search)).all()

    titles = Titles.query.all()
    return render_template('roster_test.html', roster=roster, titles=titles)