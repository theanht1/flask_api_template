from flask import Blueprint


def load_all_resources():
    """
    Include to activate api endpoint v1
    :return:
    """
    from .v1 import test


api = Blueprint("api", __name__)

load_all_resources()
