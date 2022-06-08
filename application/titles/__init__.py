from flask import Blueprint
import utils # import utils!

titles_blueprint = Blueprint('titles_assets', __name__)

from application.titles import routes