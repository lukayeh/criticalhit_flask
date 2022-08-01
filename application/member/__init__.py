from flask import Blueprint
import utils  # import utils!

member_blueprint = Blueprint("member_assets", __name__)

from application.member import routes
