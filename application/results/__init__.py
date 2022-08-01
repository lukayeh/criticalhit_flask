from flask import Blueprint
import utils  # import utils!

results_blueprint = Blueprint("results_assets", __name__)

from application.results import routes
