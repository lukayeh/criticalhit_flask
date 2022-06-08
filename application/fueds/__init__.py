from flask import Blueprint
import utils # import utils!

fueds_blueprint = Blueprint('fueds_assets', __name__)

from application.fueds import routes