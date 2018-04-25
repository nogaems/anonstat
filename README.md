# anonstat
Make statistics collection ethical again.

## Background
Nowadays collection of statistics looks more like a spying, in fact it really is. It uses all possible forms of tracking users. It starts from some easiest actions like saving your IP and even MAC-addreses. Then it goes further. People who do this are producing such horrible practices as fingerprints, based on hardware differences. For example, they are drawing little canvases in your browser for a few hundreds times in a row with mutlitple minor differences (say hello to your PC performance when you are browsing your dear facebook); you cannot even see these canvases because of their implementation, but this drawing uses your GPU directly and in various browsers paired with many GPUs this set of resulting canvases will be different. This information is used to indentify people against their will (is your favorite facebook and youtube asked your permissions for this?) and now this it not just an information, this becomes a product.

Unfortunately, advertising industry is a huge field of human activity. Due to increasing supply manufacturers are trying to increase people's demand for their products. To force people to buy things that they would never have bought normally, they don't feel ashamed to use any available methods. Giant corporations spend billions of dollars every year to lobby the laws that are convenient to them and making easier to implement their aggressive marketing politics.

The collection of statistics, that contain information about sites that got visited by users and what action those users performed there as well with further matching real people with those users — this is a precise description of the spying. And this is what international corporations are doing now. But with one little distinction, that actually people are not bothering them. People for them are not even human beings for now. They are only markening units, that could be sold and bought.

So, why these statistics are so important to them and they are ready to spend their personal money to do this? It's just because their profits increase because of this will be always more than amount of money they are spent for it, otherwise they would have been bankrupt long ago. This is how open markets work. Information, what the user has been done yesterday and what he will be interested with a high probability tomorrow, opens a vast platform for advertising networks and their activity. Corporations will pay much more money for advertisement, if it will cause more clients and purchasers of their products. And advertising targeting can provide this «improvement». Just rethink, why when you are watching some video on youtube about the videogame you would want to play, immediatelly an ad with the sale of this game appears on almost every site you are visiting often (let's just imagine that you didn't install ads blocking extention into your browser, just for this consideration)? And the important part of this — simple cookie deleting or changing IP (even MAC) won't help to prevent this, just because of the things described above. Some peole could say: «Hey, but why is this wrong? This is just comfortable, that I could do the purchase with no efforts of finding this game manually in the store!». The only thing that I could say to these people is remember the famous quote of Benjamin Franklin: «People willing to trade their freedom for temporary security deserve neither and will lose both». Is this really «safety» do not do some little «excess» efforts for usual things in your life worth this total spying?

In this situation no one is bothering about people's feelings, ethics and all these ridiculous to the media giants and ads networks things. It's just increases their profits and this is sufficient reason to do this no matter what. And just yet another sad thing is those people, who are using such tools, like Google Analytics©®™, not always are evil and often don't even want to be involved in this awful spying on the users. They are just using it in order to know how much people reading their blogs and watching their photos, and often those peole don't even know what kind of shit they are including into their personal sites.

## About
Basing on this background, people forgot, that collection of visitor statistics may be used just for showing how much people (and bots) have visited some page and may not contain any personal data. By the way, this is what exactly I'm doing here.

# Usage

## Requirements

* tornado>=4.5.1
* maxminddb>=1.3.0
* wget>=3.2
* Pillow>=3.4.2
* python-daemon>=2.1.2

## Installation

```
git clone https://github.com/nogaems/anonstat.git
cd anonstat
pip3 install --user -r requirements.txt
```

## Configuration

Then you have to edit a configuration file (`./config.py` by default). Every value that presented in the file is mandatory:

```
# The hostname and the port number of statistics server, this will be
# injected in JS plugin and used to run the server
host = 'localhost'
port = '8888'
# The list of accepted domains, that will be taken into account during
# statistics collection
domains = ['localhost']
# Timeout between two hits from the same IP (in seconds), more frequent
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
widget_update = 10
# Widget template file
widget_template = 'templates/default.py'
```

These default settings are quite good for the common usage and you can start with it.

## Preparing

Now you need to create a table for statistics in the db-file and download `GeoLite2-Country` database:

```
./manage -cv
./manage -u
```

Execute `./manage -h` for getting more options.

## Running

```
usage: anonstat [-h] [-c CONFIG] [-d] [-l LOGFILE] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Specify configuration file, './config.py' by default
  -d, --daemon          Run as a daemon
  -l LOGFILE, --logfile LOGFILE
                        Specify a log file, defaults depend on mode,if it's a
                        daemon-mode, then /dev/null is used, stdout/stderr
                        otherwise
  -e, --debug           Set logging level to DEBUG
```

# Features

* It's really anonymous. In particular, this:
    * doesn't track any user's action
    * doesn't get any user's environment variable (i.e screen resolution, browser etc)
    * doesn't send any data to some third-party services
    * doesn't write any logs about users
    * stores user's IPs only in the memory that makes it easy to clean just by restarting the server.
    ...Even if the government will require the logs from the VPS ISP they will get nothing.
* Dashboard with:
    * filtering
    * fuzzy searching
    * sorting
* Embeddable custom widgets

# Open data

After running the service you can see the dashboard at http://host:port. It contains statistics about visitors and hit count per URL for the past year.
This project licensed is under AGPL-3.0. By default everyone has an access to the dashboard, otherwise it means that service runner has changed the service code. If he/she is not going to violate the AGPL license, he/she will definitely publish all the changes he/she made. If he/she didn't, I strongly recommend don't use his/her service/site at all.
