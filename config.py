# The hostname and the port number of statistics server, this will be
# injected in JS plugin
host = 'localhost'
port = '8888'
# The list of accepted domains, that will be taken into account during
# statistics collection
domains = ['localhost']
# Timeout between two hits from the same IP (in seconds), more often
# attempts to get the same page will not affect the statistics
access_timeout = 10
# Timeout of granting a cookie for the same IP
cookie_timeout = 600
# Path to the databases
db = 'db/base.db'
geodb = 'db/GeoLite2-Country.mmdb'
# Enable https
ssl = False
# Widget update time in seconds
widget_update = 1
# Widget template file
widget_template = 'templates/default.py'
