from flask import Blueprint


def load_all_resources():
    """
    Include to activate api endpoint resources
    :return:
    """
    from .resources import test


api = Blueprint('api', __name__)

load_all_resources()
