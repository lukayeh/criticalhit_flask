from flask import Blueprint

fueds_blueprint = Blueprint("fueds_assets", __name__)

from application.fueds import routes
