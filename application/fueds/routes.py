# app/booker/routes.py
# this is where you can put all your booker routes
from re import DEBUG
from flask import render_template, request, redirect, flash, url_for
from application.fueds import fueds_blueprint
from flask import render_template
from models import *
from sqlalchemy import or_, and_, insert
from app import db

###############################################
#          Module Level Variables             #
###############################################
my_company=2

###############################################
#          Login required                     #
###############################################
from flask_login import login_required, current_user

@fueds_blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 

###############################################
#          Render fued page                   #
###############################################

@fueds_blueprint.route('/fueds')
def fueds():
    roster = Roster.query.filter(Roster.association.like(my_company)).all()
    fueds = Fueds.query.filter(Fueds.company.like(my_company)).all()

    return render_template('fueds.html', title='Fueds', roster=roster, fueds=fueds)


@fueds_blueprint.route('/create_fued/', methods=('GET', 'POST'))
def create_fued():
    company = "%{}%".format(my_company)
    roster = Roster.query.filter(
                Roster.association.like(company),
                Roster.active=='active',
                Roster.role=='wrestler').all()

    if request.method == 'POST':
        participant_1 = request.form['participant1']
        participant_2 = request.form['participant2']

        if not participant_1:
            flash('Title is required!')
        elif not participant_2:
            flash('Content is required!')
        else:
            new_fued = Fueds(
                        participant_1 = participant_1,
                        participant_2 = participant_2,
                        popularity = '0',
                        status = 'active',
                        company = my_company)

            # add the new user to the database
            db.session.add(new_fued)
            db.session.commit()

            flash(f"you have successfuly created a fued")  
            return redirect(url_for('fueds_assets.fueds'))
    return render_template('fued_create.html',roster=roster)

@fueds_blueprint.route('/delete_fued/', methods=('GET', 'POST'))
def delete_fued():
    if request.method == 'POST':
        fued_to_delete = request.form['fued_to_delete']
        print(fued_to_delete)
        if not fued_to_delete:
            flash('fued_to_delete is required!')
        else:
            delete_fued = Fueds.query.filter_by(id=fued_to_delete).first()
            delete_fued.status = 'ended'
            db.session.commit()
            flash(f"you have successfuly ended the fued")  
            return redirect(url_for('fueds_assets.fueds'))
