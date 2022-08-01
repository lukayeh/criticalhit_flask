###############################################
#          Import some packages               #
###############################################
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

###############################################
#          Module Level Variables             #
###############################################
my_company = 2

###############################################
#          Define flask app                   #
###############################################
app = Flask(__name__)

# Set up the SQLAlchemy Database to be a local file 'new_database.db'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///new_database.db"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = "auth_assets.login"
login_manager.init_app(app)

from models import User


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))


###############################################
#          Import blueprints                  #
###############################################
from application.booker import booker_blueprint

app.register_blueprint(booker_blueprint)
from application.show_booker import show_booker_blueprint

app.register_blueprint(show_booker_blueprint)
from application.roster import roster_blueprint

app.register_blueprint(roster_blueprint)
from application.member import member_blueprint

app.register_blueprint(member_blueprint)
from application.fueds import fueds_blueprint

app.register_blueprint(fueds_blueprint)
from application.results import results_blueprint

app.register_blueprint(results_blueprint)
from application.companies import companies_blueprint

app.register_blueprint(companies_blueprint)
from application.indies import indies_blueprint

app.register_blueprint(indies_blueprint)
from application.titles import titles_blueprint

app.register_blueprint(titles_blueprint)
from application.home import home_blueprint

app.register_blueprint(home_blueprint)
# blueprint for auth routes in our app
from application.auth import auth_blueprint

app.register_blueprint(auth_blueprint)

app.secret_key = "abc"


@app.route("/test")
def test():

    roster = db.Table("roster")
    # Equivalent to 'SELECT * FROM census'
    query = db.select([roster])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    print(ResultSet[:3])

    test = "temp"

    return test


###############################################
#          Disable caching                    #
###############################################


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r


###############################################
#          Define Globals                     #
###############################################
@app.context_processor
def inject_globals():
    return dict(date="15/05/2022", region="NA")


###############################################
#             Init our app                    #
###############################################
# nav.init_app(app)
bootstrap = Bootstrap5(app)

###############################################
#                Run app                      #
###############################################
if __name__ == "__main__":
    app.run(debug=True, threaded=True)
