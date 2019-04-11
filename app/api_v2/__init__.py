from flask import Blueprint


def load_all_resources():
    from .resources import test


api = Blueprint('api2', __name__)

load_all_resources()
