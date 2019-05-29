import mysql.connector

from collections import namedtuple


# TODO: Write document for this lib

class MySQLWrapper:
    """
    Wrapper lib for mysql connection
    """
    conn = None
    cur = None
    conf = None

    def __init__(self, **kwargs):
        """
        Setup database configuration

        :param kwargs:
        """
        self.conf = kwargs

    def init_app(self, current_app):
        """
        Get database configuration from flask app instance and connect to the mysql database

        :param current_app: <object> Flask app instance
        :return:
        """

        self.conf = dict(self.conf or ())

        self.conf['user'] = current_app.config.get('MYSQL_DATABASE_USERNAME')
        self.conf['password'] = current_app.config.get('MYSQL_DATABASE_PASSWORD')
        self.conf['host'] = current_app.config.get('MYSQL_DATABASE_HOST', '127.0.0.1')
        self.conf['database'] = current_app.config.get('MYSQL_DATABASE_NAME')
        self.conf['port'] = current_app.config.get('MYSQL_DATABASE_PORT', '3306')

        self.connect()

    def connect(self):
        """
        Setup connection and database cursor

        :return:
        """

        self.conn = mysql.connector.connect(**self.conf)
        self.cur = self.conn.cursor()

    def end(self):
        """Close the connection"""
        self.cur.close()
        self.conn.close()

    def _select(self, table=None, fields=(), where=None, order=None, limit=None):
        """
        Form the sql query for execution

        :param table: <string> table name
        :param fields: <list> list of selecting fields e.g. ("field1", "field2")
        :param where: <list> query condition e.g. [ "id > 1 and id < %s", 5 ]
        :param order: <list> returning order [ "id ASC", "name DESC" ]
        :param limit: <limit> number of returning items and offset of the query [5, 10]
        :return: <object> Mysql cursor object
        """
        query = "SELECT %s FROM `%s`" % (",".join(fields), table)

        # handle where query
        if where and len(where) > 0:
            query += " WHERE %s" % where[0]

        # handle order query
        if order and len(order) > 0:
            query += " ORDER BY %s" % ", ".join(order)

        # Handle limit query
        if limit and len(limit) > 0:
            query += " LIMIT %s" % limit[0]

            if len(limit) > 1:
                query += ", %s" % limit[1]

        return self.query(query, where[1] if where and len(where) > 1 else None)

    def query(self, sql, params=None, multi=False):
        """
        Run raw query

        :param sql: <string> raw sql query
        :param params: <tuple> parameters
        :param multi: <boolean> indicator for running multiple queries or not
        :return: <object> Mysql cursor object
        """

        if not multi:
            self.cur.execute(sql, params, multi=multi)
        else:
            for result in self.conn.cmd_query_iter(sql):
                continue

        return self.cur

    def get_one(self, table=None, fields='*', where=None, order=None, limit=(0, 1)):
        """
        Get single result

        :param table: <string> table name
        :param fields: <list> list of selecting fields e.g. ("field1", "field2")
        :param where: <list> query condition e.g. [ "id > 1 and id < %s", 5 ]
        :param order: <list> returning order [ "id ASC", "name DESC" ]
        :param limit: <limit> number of returning items and offset of the query [5, 10]
        :return: <namedtuple> Row object-like with fields are query fields
        """

        cur = self._select(table, fields, where, order, limit)
        result = cur.fetchone()

        row = None
        if result:
            # Create named tuple by using the query fields
            Row = namedtuple("Row", [d[0] for d in cur.description])
            row = Row(*result)

        return row

    def get_all(self, table=None, fields='*', where=None, order=None, limit=None):
        """
        Get all results

        :param table: <string> table name
        :param fields: <list> list of selecting fields e.g. ("field1", "field2")
        :param where: <list> query condition e.g. [ "id > 1 and id < %s", 5 ]
        :param order: <list> returning order [ "id ASC", "name DESC" ]
        :param limit: <limit> number of returning items and offset of the query [5, 10]
        :return: <list> A list of Row object-like with fields are query fields
        """

        cur = self._select(table, fields, where, order, limit)
        result = cur.fetchall()

        rows = None
        if result:
            # Create named tuple by using the query fields
            Row = namedtuple("Row", [d[0] for d in cur.description])
            rows = [Row(*r) for r in result]

        return rows

    def commit(self):
        """Commit a transaction"""
        return self.conn.commit()
