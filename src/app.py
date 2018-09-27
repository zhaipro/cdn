# coding: utf-8
import sqlite3

from flashtext import KeywordProcessor
from flask import Flask, g, make_response, abort

import settings


app = Flask(__name__)


def connect_db():
    rv = sqlite3.connect('db.sqlite')
    rv.text_factory = str
    rv.row_factory = sqlite3.Row
    return rv


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


def replace(body):
    if not hasattr(g, 'keyword_processor'):
        kp = KeywordProcessor()
        db = get_db()
        cur = db.execute('select DISTINCT netloc from page;')
        for netloc, in cur:
            kp.add_keyword(netloc, settings.NETLOC)
        g.keyword_processor = kp
    return g.keyword_processor.replace_keywords(body)


def get_page(path):
    if path:
        path = '/' + path
    sql = u'select type, body from page where path = ? limit 1;'
    cur = get_db().execute(sql, [path])
    page = cur.fetchone()
    if page is None:
        abort(404)
    type, body = page
    if 'text' in type:
        body = replace(body)
    return type, body


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def application(path):
    type, body = get_page(path)
    resp = make_response(body)
    resp.content_type = type
    return resp
