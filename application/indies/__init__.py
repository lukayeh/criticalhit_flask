from flask import Blueprint
import utils  # import utils!

indies_blueprint = Blueprint("indies_assets", __name__)

from application.indies import routes
