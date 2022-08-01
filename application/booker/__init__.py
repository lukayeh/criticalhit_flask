from flask import Blueprint
import utils  # import utils!

booker_blueprint = Blueprint("booker_assets", __name__)

from application.booker import routes
