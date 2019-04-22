import os
import pytest

import mysql.connector
import config.testing

from bson import json_util
from mysql.connector import errorcode

from . import AppTestClient
from app import create_app
from app.libs.mysql_wrapper import MySQLWrapper


def create_database(database, db_name):
    try:
        database.cur.execute("USE {}".format(db_name))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            try:
                database.cur.execute(
                    "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name)
                )
                database.conn.database = db_name
            except mysql.connector.Error as err:
                print("Failed creating database: {}".format(err))
                exit(1)


def init_db(database: MySQLWrapper, db_name):
    with open(os.path.join(os.path.dirname(__file__), 'data', 'data.sql'), 'rb') as f:
        _data_sql = f.read().decode('utf8')

    # Select database
    create_database(database, db_name)

    # Init test data
    if _data_sql:
        database.query(_data_sql, multi=True)


def init_mongo_db(app):
    from app.models.mongo import mongo, mongo_db

    # Clear previous test data
    mongo.drop_database(app.config['MONGO_DATABASE_NAME'])

    dir_path = os.path.join(os.path.dirname(__file__), 'data')
    for file in os.listdir(dir_path):
        if file.endswith(".json"):
            # Insert data
            data = []
            with open(os.path.join(dir_path, file)) as f:
                for line in f.readlines():
                    data.append(json_util.loads(line))

            if len(data):
                mongo_db[file.strip('.json')].insert_many(data)


def clear_db(database, conf):
    """Clear test data"""
    from app.models.mongo import mongo
    from app import mysql_db

    if mysql_db is not None:
        # Close app db connection
        mysql_db.end()

    database.query('DROP DATABASE %s' % conf['MYSQL_DATABASE_NAME'])
    database.end()

    mongo.drop_database(conf['MONGO_DATABASE_NAME'])


def get_db():
    # Create mock data
    import config.testing
    conf = {
        'user': config.testing.MYSQL_DATABASE_USERNAME,
        'password': config.testing.MYSQL_DATABASE_PASSWORD,
        'host': config.testing.MYSQL_DATABASE_HOST,
        'port': config.testing.MYSQL_DATABASE_PORT
    }

    db_wrapper = MySQLWrapper(**conf)
    db_wrapper.connect()

    return db_wrapper


@pytest.fixture
def app():
    mysql_db = get_db()
    init_db(mysql_db, config.testing.MYSQL_DATABASE_NAME)

    app = create_app('testing')

    # Create and load test data
    with app.app_context():
        init_mongo_db(app)

    yield app

    # Clear temporary database
    clear_db(mysql_db, app.config)


@pytest.fixture
def client(app):
    return AppTestClient(app, app.config['USERNAME'], app.config['PASSWORD'])


@pytest.fixture
def db(app):
    import config.testing

    conf = {
        'user': config.testing.MYSQL_DATABASE_USERNAME,
        'password': config.testing.MYSQL_DATABASE_PASSWORD,
        'host': config.testing.MYSQL_DATABASE_HOST,
        'port': config.testing.MYSQL_DATABASE_PORT,
        'database': config.testing.MYSQL_DATABASE_NAME
    }

    db = MySQLWrapper(**conf)
    db.connect()

    yield db

    db.end()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
