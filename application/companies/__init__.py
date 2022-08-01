from flask import Blueprint

companies_blueprint = Blueprint("companies_assets", __name__)

from application.companies import routes
