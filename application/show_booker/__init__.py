from flask import Blueprint
import utils # import utils!

show_booker_blueprint = Blueprint('show_booker_assets', __name__)

from application.show_booker import routes