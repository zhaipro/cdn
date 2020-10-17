# coding: utf-8
import random
import sqlite3
import urllib

from flashtext import KeywordProcessor
from flask import Flask, g, make_response, abort, redirect, request

import settings


app = Flask(__name__)


def _str(s):
    try:
        return s.decode('utf-8')
    except:
        return s


def connect_db():
    rv = sqlite3.connect(settings.DATABASE)
    rv.text_factory = _str
    rv.row_factory = sqlite3.Row
    return rv


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'webpage_db'):
        g.webpage_db.close()


def get_db():
    if not hasattr(g, 'webpage_db'):
        g.webpage_db = connect_db()
    return g.webpage_db


def replace(body):
    if not hasattr(g, 'keyword_processor'):
        kp = KeywordProcessor()
        db = get_db()
        cur = db.execute('select DISTINCT netloc from page;')
        for netloc, in cur:
            kp.add_keyword(netloc, settings.NETLOC)
        g.keyword_processor = kp
    return g.keyword_processor.replace_keywords(body)


def get_random():
    db = get_db()
    if not hasattr(get_random, 'c'):
        get_random.c = db.execute('select count(*) from page where type = "image/jpeg" and netloc = ?;', [settings.START_URL[7:]]).fetchone()[0]
    sql = 'select body from page where type = "image/jpeg" and netloc = ? limit 1 offset ?;'
    while True:
        x = random.randint(0, get_random.c - 1)
        body, = db.execute(sql, [settings.START_URL[7:], x]).fetchone()
        if len(body) > 20 * 1024:
            break
    return body


def get_page(path):
    if path:
        path = '/' + path
    # 有些脚本是通过参数动态加载的
    sql = 'select type, body from page where upper(path) = upper(?) and query = ? limit 1;'
    # 为什么 type(request.query_string) == bytes
    query_string = request.query_string.decode()
    cur = get_db().execute(sql, [path, query_string])
    page = cur.fetchone()
    if page is None:
        abort(404)
    _type, body = page
    if 'text' in _type:
        body = replace(body)
    return _type, body


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def application(path):
    path = urllib.parse.quote(path)
    if path == 'random.html':
        with open('random.html', encoding='utf-8') as fp:
            body = fp.read()
        resp = make_response(body)
        resp.connect_type = 'text/html; charset=UTF-8'
        return resp
    if path == 'random':
        body = get_random()
        resp = make_response(body)
        resp.content_type = 'image/jpeg'
        return resp
    try:
        _type, body = get_page(path)
        resp = make_response(body)
        resp.content_type = _type
    except:
        resp = redirect(urllib.parse.urljoin(settings.START_URL, path))
    return resp


if __name__ == '__main__':
    host = settings.NETLOC
    port = 80
    if ':' in host:
        host, port = host.split(':')
    app.run(host=host, port=port)
