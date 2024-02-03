from flask import Blueprint
bp = Blueprint('crud', __name__)
from app.crud import routes