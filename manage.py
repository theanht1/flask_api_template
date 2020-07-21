import os

import click
from flask.cli import FlaskGroup

from app import create_app


def create_flask_app():
    app = create_app(os.environ.get("FLASK_API_ENV", "development"))

    @app.cli.command()
    def deploy():
        """
        Run deployment tasks
        :return:
        """
        pass


@click.group(cls=FlaskGroup, create_app=create_flask_app)
def cli():
    """This is a management script for the seo application"""


if __name__ == "__main__":
    cli()
