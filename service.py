#!/usr/bin/env python3
# coding: utf-8

import tornado.ioloop
import tornado.web
from tornado.gen import coroutine
import config as cfg
import sqlite3
import os
import time
import maxminddb


class Index(tornado.web.RequestHandler):

    def get(self):
        self.render('test.html')


class Service(tornado.web.RequestHandler):
    ip = {}
    reader = maxminddb.open_database(cfg.geodb)
    db = sqlite3.connect(cfg.db)

    @coroutine
    def post(self):
        if self.request.remote_ip in self.ip.keys() and \
                time.time() - self.ip[self.request.remote_ip] <= cfg.timeout:
            self.set_status(403, reason='Timeout')
        elif not self.get_cookie('SID'):
            self.set_status(403, reason='The lack of cookie')
        else:
            self.ip[self.request.remote_ip] = time.time()
            if not self.request.host_name in cfg.domains:
                self.set_status(403, 'Unaccepted domain')
            else:
                self.dump(self.request)
                self.set_status(200)

    def dump(self, request):
        data = (request.body,
                request._start_time,
                request.cookies.get("SID").value,
                self.get_country(request.remote_ip),
                )
        print(data)
        cur = self.db.cursor()
        cur.execute('''
        INSERT INTO stats VALUES(?,?,?,?);
        ''', data)
        cur.execute("PRAGMA wal_checkpoint(PASSIVE)")
        self.db.commit()

    def get_country(self, ip):
        result = self.reader.get(ip)
        return result['country']['names']['en'] if result else 'Undefined'


class Script(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        self.set_header('Content-Type', 'text/javascript')
        self.render(
            'counter.js', host=cfg.host, port=cfg.port, ssl='s' if cfg.ssl else '')


class Widget(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        pass

# TODO: replace to manage.py


def create_db(connection):
    c = connection.cursor()
    c.execute(
        '''
    CREATE TABLE IF NOT EXISTS stats
        (url TEXT, time REAL, id TEXT, country TEXT);
    '''
    )
    c.execute("PRAGMA wal_checkpoint(PASSIVE)")
    c.close()

db = sqlite3.connect('db/base.db')
create_db(db)

if __name__ == "__main__":
    app = tornado.web.Application(
        [
            (r'/', Index),
            (r'/bump', Service),
            (r'/anonstat.js', Script),
            (r'/gidget', Widget)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates")

    )
    app.listen(cfg.port)
    tornado.ioloop.IOLoop.current().start()
