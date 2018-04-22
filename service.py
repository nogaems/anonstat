#!/usr/bin/env python3
# coding: utf-8

import tornado.ioloop
import tornado.web
from tornado.gen import coroutine
import maxminddb

import sqlite3
import os
import time
import random
import hashlib
from io import BytesIO

import config as cfg
from widget import Context
random = random.SystemRandom()
random.seed()
cookie_secret = hashlib.sha256(str(random.random()).encode('utf8')).hexdigest()


class Index(tornado.web.RequestHandler):

    def get(self):
        self.render('test.html')


class Service(tornado.web.RequestHandler):
    access = {}
    grants = {}
    sids = [None]
    reader = maxminddb.open_database(cfg.geodb)
    db = sqlite3.connect(cfg.db)

    @coroutine
    def post(self):
        if not self.request.remote_ip in self.access.keys():
            if not self.request.host_name in cfg.domains:
                self.set_status(403, 'Unaccepted domain')
                return
            sid = self.grant_sid()
        else:
            if time.time() - self.access[self.request.remote_ip] <= cfg.access_timeout:
                self.set_status(403, reason='Access timeout')
                return
            sid = self.get_secure_cookie('SID')
            sid = sid.decode('utf-8') if sid else None
            if not sid in self.sids:
                self.set_status(403, reason='Invalid cookie')
                return
            if not sid:
                if time.time() - self.grants[self.request.remote_ip] <= cfg.cookie_timeout:
                    self.set_status(403, reason='Cookie granting timeout')
                    return
                sid = grant_sid()
        self.access[self.request.remote_ip] = time.time()
        self.set_status(200)
        self.dump(self.request.body,
                  self.request._start_time,
                  sid,
                  self.get_country(self.request.remote_ip)
                  )

    def dump(self, *args):
        print(*args)
        cur = self.db.cursor()
        cur.execute('''
        INSERT INTO stats VALUES(?,?,?,?);
        ''', args)
        cur.execute("PRAGMA wal_checkpoint(PASSIVE)")
        self.db.commit()

    def get_country(self, ip):
        result = self.reader.get(ip)
        return result['country']['names']['en'] if result else 'Undefined'

    def get_random_bytes(self, length=16):
        return ''.join([hex(random.randint(0, 15))[2:] for _ in range(length)])

    def grant_sid(self):
        sid = self.get_random_bytes()
        self.sids.append(sid)
        self.grants[self.request.remote_ip] = time.time()
        self.set_secure_cookie('SID', sid, expires_days=365)
        return sid


class Script(tornado.web.RequestHandler):

    @coroutine
    def get(self):
        self.set_header('Content-Type', 'text/javascript')
        self.render(
            'counter.js', host=cfg.host, port=cfg.port, ssl='s' if cfg.ssl else '')


class Widget(tornado.web.RequestHandler):
    widget = {'timestamp': None, 'image': None}

    def __init__(self, *args, **kwargs):
        self.cache(self.render())
        super(Widget, self).__init__(*args, **kwargs)

    @coroutine
    def get(self):
        if time.time() - self.widget['timestamp'] > cfg.widget_update:
            out = self.render()
            self.cache(out)
        else:
            out = self.widget['image']
        self.set_header('Content-Type', 'image/png')
        self.write(out)

    def render(self):
        data = {
            'uday': 1234,
            'uweek': 1234,
            'umonth': 1234,
            'hday': 1234,
            'hweek': 1234,
            'hmonth': 1234
        }
        c = Context()
        out = BytesIO()
        img = c.draw_small(data)
        img.save(out, 'PNG')
        return out.getvalue()

    def cache(self, img):
        self.widget['timestamp'] = time.time()
        self.widget['image'] = img


if __name__ == "__main__":
    app = tornado.web.Application(
        [
            (r'/', Index),
            (r'/bump', Service),
            (r'/anonstat.js', Script),
            (r'/widget.png', Widget)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        cookie_secret=cookie_secret

    )
    app.listen(cfg.port)
    tornado.ioloop.IOLoop.current().start()
