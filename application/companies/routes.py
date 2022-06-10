# app/booker/routes.py
# this is where you can put all your booker routes
from flask import render_template, request, redirect, flash, url_for
from application.companies import companies_blueprint
from flask import render_template
from models import *

###############################################
#          Login required                     #
###############################################
from flask_login import login_required, current_user

@companies_blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

###############################################
#          Render companies page              #
###############################################
@companies_blueprint.route('/companies')
def companies():
    companies = Companies.query.all()
    print(companies)
    return render_template('companies.html', title='Companies', companies=companies)
