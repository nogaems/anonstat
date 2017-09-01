# The hostname and the port number of statistics server, this will be
# injected in JS
host = 'localhost'
port = '8888'
# The list of accepted domains, that will be taken into accout during
# statistics collection
domains = ['localhost']
# Timeout between two hits from the same IP (in seconds), more often
# attempts to get a page will not affect the statistics
timeout = 10
# Path to the databases
db = 'db/base.db'
geodb = 'db/GeoLite2-Country.mmdb'
ssl = False
