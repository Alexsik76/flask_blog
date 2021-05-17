from flask import Blueprint

db = Blueprint('auth', __name__)

from app.auth import routes
