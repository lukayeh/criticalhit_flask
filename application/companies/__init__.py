from flask import Blueprint
import utils # import utils!

companies_blueprint = Blueprint('companies_assets', __name__)

from application.companies import routes