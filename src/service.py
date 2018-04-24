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
import imp
from urllib.parse import urlparse

import config as cfg
from widget import Template

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

    @coroutine
    def post(self):
        if not self.request.remote_ip in self.access.keys():
            if urlparse(self.request.body).hostname.decode('utf8') not in cfg.domains:
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
                  int(self.request._start_time),
                  sid,
                  self.get_country(self.request.remote_ip)
                  )

    def dump(self, *args):
        print(*args)
        db = sqlite3.connect(os.path.abspath(cfg.db))
        cur = db.cursor()
        cur.execute('''
        INSERT INTO stats VALUES(?,?,?,?);
        ''', args)
        cur.execute("PRAGMA wal_checkpoint(PASSIVE)")
        db.commit()
        db.close()

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
    template = None
    db = sqlite3.connect(cfg.db)

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
        template = imp.load_source('template', cfg.widget_template)
        context = Template(template.render,
                           template.extractors)
        data = self.get_data(template.extractors)
        out = BytesIO()
        img = context.render(data)
        img.save(out, 'PNG')
        return out.getvalue()

    def get_data(self, extractors):
        data = {}
        db = sqlite3.connect(cfg.db)
        cur = db.cursor()
        for key in extractors:
            cur.execute(extractors[key])
            result = cur.fetchall()[0][0]
            result = result if result is not None else 'N/A'
            data[key] = result
        return data

    def cache(self, img):
        self.widget['timestamp'] = time.time()
        self.widget['image'] = img
