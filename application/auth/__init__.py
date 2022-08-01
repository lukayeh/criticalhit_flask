from flask import Blueprint
import utils  # import utils!

auth_blueprint = Blueprint("auth_assets", __name__)

from application.auth import routes
