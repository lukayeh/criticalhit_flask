# app/booker/routes.py
# this is where you can put all your booker routes
from flask import render_template, request, redirect, flash, url_for
from application.booker import post_runner  # importing the runner
from application.booker import tagmatch  # importing the runner
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


@booker_blueprint.route("/booker_home")
def booker_home():
    return render_template("booker_home.html")

@booker_blueprint.route("/booker_tag_post", methods=["POST"])
def booker_tag_post():

    team1_01 = request.form["participant1"]
    team1_02 = request.form["participant2"]

    team2_01 = request.form["participant3"]
    team2_02 = request.form["participant4"]

    tagteams = {}
    tagteams[f"team_1"] = {}
    tagteams[f"team_1"]["member_1"] = {}
    tagteams[f"team_1"]["member_2"] = {}
    tagteams[f"team_1"]["member_1"]["id"] = f"{team1_01}"
    tagteams[f"team_1"]["member_2"]["id"] = f"{team1_02}"

    tagteams[f"team_2"] = {}
    tagteams[f"team_2"]["member_1"] = {}
    tagteams[f"team_2"]["member_2"] = {}
    tagteams[f"team_2"]["member_1"]["id"] = f"{team2_01}"
    tagteams[f"team_2"]["member_2"]["id"] = f"{team2_02}"

    for t_id, t_info in tagteams.items():
        print("Team:", t_id)
        for key in t_info:
            print(t_info[key]["id"])
            member = Roster.query.filter_by(id=t_info[key]["id"]).first()
            tagteams[t_id][key] = member
    print(tagteams)
    bonus = 0

    # Retrieve moves list
    moves = Moves.query.all()
    moves_list = []
    for move in moves:
        moves_list.append(move.name)

    booker = tagmatch.Booker(participants=tagteams, moves=moves_list, bonuses=bonus)

    # Add to the result table
    booker_string = ",".join(map(str, booker.roundup))
    winners = str(booker.winner[0] + " & " + booker.winner[1])
    losers = str(booker.loser[0] + " & " + booker.loser[1])
    result =  str(booker.winner[0] + " & " + booker.winner[1] + " defeats " + booker.loser[0] + " & " + booker.loser[1])
    new_result = Result(
        result=result,
        rating=booker.stars,
        winner=winners,
        loser=losers,
        description=booker_string,
    )
    db.session.add(new_result)

    # # Update the loser
    for x in booker.loser:
        update_loser = Roster.query.filter_by(name=x).first()
        update_loser.health = (update_loser.health) - 5
        update_loser.losses = update_loser.losses + 1
        update_loser.morale = update_loser.morale - 5
    # # Update the winner
    for x in booker.winner:
        update_winner = Roster.query.filter_by(name=x).first()
        update_winner.level = update_winner.level + 1
        update_winner.wins = update_winner.wins + 1

    db.session.commit()

    return render_template("booker_tag_post.html", tag_teams=tagteams, booker=booker)


###############################################
#          Render Booker_tag page                 #
###############################################
@booker_blueprint.route("/booker_tag")
def booker_tag():

    company = "%{}%".format(my_company)
    roster = Roster.query.filter(
        Roster.association.like(company),
        Roster.active == "active",
        Roster.role == "wrestler",
    ).all()
    titles = Titles.query.all()
    return render_template(
        "booker_tag.html", title="Booker", roster=roster, titles=titles
    )


###############################################
#          Render Booker page                 #
###############################################
@booker_blueprint.route("/booker")
def booker():

    company = "%{}%".format(my_company)
    roster = Roster.query.filter(
        Roster.association.like(company),
        Roster.active == "active",
        Roster.role == "wrestler",
    ).all()
    titles = Titles.query.all()
    return render_template("booker.html", title="Booker", roster=roster, titles=titles)


###############################################
#          Render booker_post page            #
###############################################
@booker_blueprint.route("/booker_post", methods=["POST"])
def booker_post():
    participants_sql = Roster.query.filter(
        or_(
            Roster.id == request.form["participant1"],
            Roster.id == request.form["participant2"],
        )
    ).all()

    ## Update rating if they're in a fued!
    fueds = Fueds.query.filter(
        or_(
            (
                and_(
                    Fueds.participant_1 == request.form["participant1"],
                    Fueds.participant_2 == request.form["participant2"],
                )
            ),
            (
                and_(
                    Fueds.participant_1 == request.form["participant2"],
                    Fueds.participant_2 == request.form["participant1"],
                )
            ),
        )
    ).all()

    ## Grab titles
    titles = Titles.query.all()

    # set bonus to 0
    bonus = 0

    # Setup a titles list
    myTitles = []

    # Check for titles
    if "titlematch" in request.form or "titlematch_2" in request.form:
        print(f"titlematch set")

        # Append first title
        if "titlematch" in request.form:
            # Append first title
            myTitles.append(request.form["titlematch"])

        # Append second title
        if "titlematch_2" in request.form:
            # Append second title
            myTitles.append(request.form["titlematch_2"])

        # print(myTitles)
        joinedTitles = ",".join(myTitles)
        # print(joinedTitles)
        bonus = bonus + 5
        flash(f"Title bonus added +5!")
    else:
        print(f"titlematch NOT set")
        titlematch = "false"

    # Check for omg moment
    if "omgmoment" in request.form:
        print(f"OMG moment set")
        omgmoment = "true"
        bonus = bonus + 5
    else:
        print(f"OMG moment NOT set")
        omgmoment = "false"

    # Check for run in moment
    if "run_in" in request.form:
        print(f"Random run_in moment set")
        # rand = random.randrange(0, Roster.query.count()) 
        # runner = Roster.query.filter(Roster.id == request.form[rand]).all()
        # print(runner)
        runin_moment = "true"
        bonus = bonus + 5
    else:
        print(f"Random run_in moment NOT set")
        runin_moment = "false"

    # Check if the participants are in a fued if so give extra points!
    if fueds:
        print(f"They are in a fued together")
        bonus = bonus + 10
        fued_bonus = "true"
    else:
        fued_bonus = "false"
        print(f"No fued found")

    # Retrieve moves list
    moves = Moves.query.all()
    moves_list = []
    for move in moves:
        moves_list.append(move.name)

    stipulation=""

    booker = post_runner.Booker(
        participants=participants_sql,
        bonuses=bonus,
        omgmoment=omgmoment,
        runin_moment=runin_moment,
        moves=moves_list,
        stipulation=stipulation,
    )

    print(booker.winner)
    booker_string = ",".join(map(str, booker.roundup))

    # conn.execute("INSERT INTO result (result, rating, description) VALUES (?, ?, ?)", [booker[2], booker[5], booker_string])

    # Add to the result table
    new_result = Result(
        result=booker.result,
        rating=booker.stars,
        winner=booker.winner,
        loser=booker.loser,
        description=booker_string,
    )
    db.session.add(new_result)
    # Update the loser
    update_loser = Roster.query.filter_by(name=booker.loser).first()
    update_loser.health = (update_loser.health) - 5
    update_loser.losses = update_loser.losses + 1
    update_loser.morale = update_loser.morale - 5
    # Update the winner
    update_winner = Roster.query.filter_by(name=booker.winner).first()
    update_winner.level = update_winner.level + 1
    update_winner.wins = update_winner.wins + 1

    # Update titles
    if "titlematch" in request.form or "titlematch_2" in request.form:
        update_loser.accolade = "none"
        update_winner.accolade = joinedTitles

    db.session.commit()

    if fued_bonus == "true":
        flash(f"Fued bonus added +10!")
    return render_template(
        "booker_post.html",
        title="Booker",
        booker=booker,
        participants=participants_sql,
        myTitles=myTitles,
        titles=titles,
    )
