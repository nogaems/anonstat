#!/usr/bin/env python3
# coding: utf8

import wget

import argparse
import sqlite3
import tarfile
import os
import config as cfg

geolite_url = 'http://geolite.maxmind.com/download/geoip/database/GeoLite2-Country.tar.gz'


def serve(code):

    def wrapper(name='stats', verbose=False, ask=True):
        c = code(name)
        if verbose:
            print(c)
        if ask:
            if not confirm():
                return
        conn = sqlite3.connect(cfg.db)
        cursor = conn.cursor()
        cursor.execute(c)
        cursor.execute("PRAGMA wal_checkpoint(PASSIVE)")
        conn.commit()
        conn.close()
    return wrapper


@serve
def create_db(name='stats'):
    return '''
        CREATE TABLE IF NOT EXISTS {}
        (url TEXT, time REAL, id TEXT, country TEXT);
        '''.format(name)


@serve
def drop_db(name='stats'):
    return '''
        DROP TABLE IF EXISTS {};
        '''.format(name)


def confirm():
    answer = input('Are you sure? [Y]/n: ')
    while answer and (not answer in 'yYnN'):
        answer = input('[Y]/n:')
    return True if not answer or answer in 'yY' else False

parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                 description='Manage script')
parser.add_argument('-c', '--create', action='store_true',
                    help='Create `stats` database')
parser.add_argument('-d', '--drop', action='store_true',
                    help='Drop `stats` database')
parser.add_argument('-u', '--update', action='store_true',
                    help='Update `GeoLite2-Country` database')
parser.add_argument('-f', '--force', action='store_true',
                    help='Don\'t ask')
parser.add_argument('-v', '--verbose', action='store_true',
                    help='Verbose output')

args = parser.parse_args()

if args.create:
    create_db(verbose=args.verbose, ask=not args.force)
elif args.drop:
    drop_db(verbose=args.verbose, ask=not args.force)
elif args.update:
    print('Fetching: \'{}\''.format(geolite_url))
    tarname = wget.download(geolite_url)
    tar = tarfile.open(tarname, 'r:gz')
    base = [item for item in tar if item.name.endswith('.mmdb')]
    base = tar.extractfile(base[0])
    open(cfg.geodb, 'wb').write(base.read())
    os.remove(tarname)
else:
    parser.print_usage()
