import psycopg2
import psycopg2.extras

import click
from flask import current_app
from flask import g
from flask.cli import with_appcontext


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = psycopg2.connect(
            current_app.config["DATABASE"]
        )
        g.cur = g.db.cursor(cursor_factory = psycopg2.extras.DictCursor)

    return g.db, g.cur
