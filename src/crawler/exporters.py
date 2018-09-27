import sqlite3
import time
from urlparse import urlparse

from scrapy.exporters import BaseItemExporter


class SqliteItemExporter(BaseItemExporter):

    def __init__(self, file, **kws):
        self.file = file
        super(SqliteItemExporter, self).__init__(**kws)

    def export_item(self, item):
        sql = 'insert or ignore into page(netloc, path, query, type, body) values(?, ?, ?, ?, ?);'
        _, netloc, path, _, query, _ = urlparse(item['url'])
        self.conn.execute(sql, (netloc, path, query, item['type'], item['body']))
        if time.time() - self.last_time > 5:
            self.conn.commit()
            self.last_time = time.time()

    def start_exporting(self):
        self.file.close()
        self.conn = sqlite3.connect(self.file.name)
        self.conn.text_factory = str
        fields = ['id integer primary key autoincrement',
                  'netloc', 'path', 'query', 'type', 'body']
        sql = 'create table if not exists page(%s);' % ', '.join(fields)
        self.conn.execute(sql)
        self.conn.commit()
        self.last_time = time.time()

    def finish_exporting(self):
        self.conn.commit()
        self.conn.close()
