import mysql.connector

from collections import namedtuple


class MySQLWrapper:
    conn = None
    cur = None
    conf = None

    def __init__(self, **kwargs):
        self.conf = kwargs

    def init_app(self, current_app):
        self.conf = {
            'user': current_app.config.get('MYSQL_DATABASE_USERNAME'),
            'password': current_app.config.get('MYSQL_DATABASE_PASSWORD'),
            'host': current_app.config.get('MYSQL_DATABASE_HOST', '127.0.0.1'),
            'database': current_app.config.get('MYSQL_DATABASE_NAME'),
            'port': current_app.config.get('MYSQL_DATABASE_PORT', '3306')
        }
        self.connect()

    def connect(self):
        self.conn = mysql.connector.connect(**self.conf)
        self.cur = self.conn.cursor()

    def end(self):
        """Close the connection"""
        self.cur.close()
        self.conn.close()

    def _select(self, table=None, fields=(), where=None, order=None, limit=None):
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
        """Run raw query"""

        if not multi:
            self.cur.execute(sql, params, multi=multi)
        else:
            for result in self.conn.cmd_query_iter(sql):
                continue

        return self.cur

    def getOne(self, table=None, fields='*', where=None, order=None, limit=(0, 1)):
        """ Get single result """

        cur = self._select(table, fields, where, order, limit)
        result = cur.fetchone()

        row = None
        if result:
            Row = namedtuple("Row", [d[0] for d in cur.description])
            row = Row(*result)

        return row

    def getAll(self, table=None, fields='*', where=None, order=None, limit=None):
        """ Get all results """
        cur = self._select(table, fields, where, order, limit)
        result = cur.fetchall()

        rows = None
        if result:
            Row = namedtuple("Row", [d[0] for d in cur.description])
            rows = [Row(*r) for r in result]

        return rows

    def commit(self):
        """Commit a transaction"""
        return self.conn.commit()
