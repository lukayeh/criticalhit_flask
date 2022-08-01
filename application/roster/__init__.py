from flask import Blueprint
import utils  # import utils!

roster_blueprint = Blueprint("roster_assets", __name__)

from application.roster import routes
