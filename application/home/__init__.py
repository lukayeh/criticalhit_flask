from flask import Blueprint
import utils # import utils!

home_blueprint = Blueprint('home_assets', __name__)

from application.home import routes