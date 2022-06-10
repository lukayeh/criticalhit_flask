# app/booker/routes.py
# this is where you can put all your booker routes
from flask import render_template, request, redirect, flash, url_for
from application.member import member_blueprint
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

@member_blueprint.before_request
@login_required
def before_request():
    """ Protect all of the admin endpoints. """
    pass 


###############################################
#          Render member page                 #
###############################################
@member_blueprint.route('/member')
def member():
    member = Roster.query.filter(Roster.id.like(request.args['member_id'])).all()
    titles = Titles.query.all()
    associations = Companies.query.all()

    return render_template('member.html', title='Member', member=member, titles=titles, companies=associations)

# Hire Worker
@member_blueprint.route('/hire_member/', methods=('GET', 'POST'))
def hire_member():
    if request.method == 'POST':
        worker_to_hire = request.form['worker_to_hire']
        worker_name = request.form['worker_name']
        print(worker_to_hire)
        if not worker_to_hire:
            flash('worker_to_hire is required!')
        else:
            # Hire worker
            hire_worker = Roster.query.filter_by(id=worker_to_hire).first()
            hire_worker.association = my_company            
            db.session.commit()

            flash(f"you are successfuly hired {worker_name}")  
            return redirect(url_for('roster_assets.roster'))

@member_blueprint.route('/fire_member/', methods=('GET', 'POST'))
def fire_member():
    if request.method == 'POST':
        worker_to_fire = request.form['worker_to_fire']
        worker_name = request.form['worker_name']
        print(worker_to_fire)
        if not worker_to_fire:
            flash('worker_to_fire is required!')
        else:
            # Fire worker
            fire_worker = Roster.query.filter_by(id=worker_to_fire).first()
            fire_worker.association = 0            
            db.session.commit()

            flash(f"you are successfuly fired {worker_name}")  
            return redirect(url_for('roster_assets.roster'))

@member_blueprint.route('/edit_member/', methods=('GET', 'POST'))
def edit_member():
    worker_to_edit = request.args['member_id']
    member = Roster.query.filter(Roster.id.like(worker_to_edit)).all()
        
    return render_template('member_edit.html',
                            member=member)

@member_blueprint.route('/submit_member/', methods=('GET', 'POST'))
def submit_member():
    # print(request.method)
    if request.method == 'POST':
        update_roster=Roster.query.filter(Roster.id == request.form['id']).update({
                'name': request.form['name'],
                'real_name': request.form['realName'],
                'role': request.form['role'],
                'association': request.form['association'],
                'accolade': request.form['accolade'],
                'active': request.form['accolade'],
                'finisher': request.form['finisher'],
                'attack': request.form['attack'],
                'defense': request.form['defense'],
                'health': request.form['health'],
                'level': request.form['level'],
                'wins': request.form['wins'],
                'losses': request.form['losses'],
                'img': request.form['img']
                })

        print(update_roster)
        db.session.commit()

        flash(f"you have successfuly updated member {request.form['name']}")  
    return redirect(url_for('roster_assets.roster'))
