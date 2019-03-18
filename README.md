# anonstat
Make statistics collection ethical again.

## Background
Nowadays collection of statistics looks more like a spying, in fact it actually is. It uses all possible forms of tracking users. It starts with some primitive actions like saving your IP and even MAC-addreses, but then it goes further. For example, people who do this are producing such horrible practices as fingerprints, based on hardware differences. In essence, they are drawing little canvases in your browser for a few hundred times in a row with mutlitple minor differences (say hello to your PC performance when you are browsing your favorite sites). You cannot even see these canvases because of their implementation, but this drawing uses your GPU directly and in various browsers combined with different hardware information (like your CPU model and stuff) the set of resulting information will vary among machines and environments. This information is used to indentify people against their will (has facebook or youtube asked your consent for this?) and at that point this it not just an information set anymore, this becomes a product.

Unfortunately, the advertising industry is a huge field of human activity. Due to the increasing supply manufacturers are trying to increase people's demand for their products. To force people to buy things that they would never have bought normally, they don't feel ashamed to use any available methods. Giant corporations spend billions of dollars every year to lobby the laws that are convenient to them and making it easier to deploy their aggressive marketing politics.

The collection of statistics containing information about sites that got visited by users and what action those users performed there along with further matching real people with those users — this is the exact description of the internet spying. And this is what international corporations are doing now. But with one little distinction that the actual people don't really bother them. People for them are not even human beings at that point. They are only marketing units that could be sold and bought.

So, why are those statistics that important to them and they are actually ready to spend their personal money to perform this? It's dead simple: their profits increase because of those actions is more than the amount of money they have spent for it, otherwise they would have been bankrupted long time ago. This is how the open market works. The information about what a user was doing yesterday and what he will be interested in with a high probability tomorrow opens a vast platform for advertising networks and their activity. Corporations will pay much more money for this sort of advertisement if it causes more clients and purchasers for their products compared to any regular methods. And the advertising targeting can provide such an «improvement». Just rethink, why when you are watching some video on youtube about the videogame you would want to play there is immediatelly an ad pops up with the sale of this game? And it appears on almost every site you visit (let's just imagine that you didn't install any ad blocking extention into your browser, just for this consideration)? And the important part of this — simple cookie deleting or changing IP (even MAC) won't help to prevent this, just because of the things described above. Some people may say: «Hey, but why is this wrong? This is just comfortable that I can purchase this game  without efforts of finding it myself in the store!». The only thing that I could say to these people is remember the famous quote of Benjamin Franklin: «People willing to trade their freedom for temporary security deserve neither and will lose both». Does this «safety» from making  any «excess» efforts for usual things in your life worth the total spying on you? Would you actually buy this game or that ad was a decisive factor for you to do so?

In this situation no one is bothering about people's feelings, ethics and all these ridiculous for the media giants and ads networks things. It merely increases their profits and this is a sufficient reason to do anything no matter what. And just yet another sad thing is those people, who are using such tools, like Google Analytics©®™, not necessarily are evil and often don't even want to be involved in this awful spying on the users. They are just using it in order to get to know how many people read their blogs and watched their photos. Moreover, often those peole don't even know what kind of shit they are putting onto their sites.

## About
People forgot that collection of visitor statistics may be used just for showing how much people (and bots) have visited some page and may don't contain personal and sensitive in any regarding data. By the way, this is exactly what I'm doing here.

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

Then you have to edit a configuration file (`./config.py` by default). Every value presented in the file is mandatory:

```
# The hostname and the port number of statistics server, this will be
# injected in JS plugin and used to run the server
host = 'localhost'
port = '8888'
# The list of accepted domains, that will be taken into account during
# statistics collection, requests from domains that were not listed
# will be refused
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

These default settings are quite good for testing and should be considered as an example.

## Preparing

Now you need to create a table for statistics in the db-file and download `GeoLite2-Country` database:

```
./manage -cv
./manage -u
```

Execute `./manage -h` for getting more options.

## Client side

To make a page send statistics, just insert the script into it like that:

```
...
<head>
...
<script src="http://host:port/anonstat.js"></script>
...
</head>
...

```

where `host` and `port` are the values from the config.

## Running

```
usage: anonstat [-h] [-c CONFIG] [-d] [-l LOGFILE] [-e]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Specify a configuration file, './config.py' by default
  -d, --daemon          Run as a daemon
  -l LOGFILE, --logfile LOGFILE
                        Specify a log file, defaults depend on mode, if it's
                        daemon-mode, then /dev/null is used, stdout/stderr
                        otherwise
  -e, --debug           Set logging level to DEBUG
```

# Features

* It's really anonymous. In particular, it:
    * doesn't track any user's action
    * doesn't get any user's environment variable (i.e screen resolution, browser etc)
    * doesn't send any data to some third-party services
    * doesn't write any logs about users
    * stores user's IPs only in the memory that makes it easy to clean just by restarting the server.

    Even if the government will require the logs from the VPS ISP they will get nothing.
* Dashboard with:
    * filtering
    * fuzzy searching
    * sorting
* Embeddable custom widgets
* Open data

   After running the service you can see the dashboard at http://host:port. It contains statistics about visitors and hit count per URL for the past year.
   This project licensed is under AGPL-3.0. By default everyone has an access to the dashboard, otherwise it means that the service runner has changed the service code. If he/she is not going to violate the AGPL license, he/she will definitely publish all the changes he/she made. If he/she didn't, I strongly recommend to not use his/her service/site at all.
