from bs4 import BeautifulSoup
from re import findall
from json import loads
<<<<<<< HEAD
#import logging
#from datetime import datetime

def Follow(response):
    #logging.info("[<] " + str(datetime.now()) + ':: feed+Follow')
=======

import logging as logme

def Follow(response):
    logme.debug(__name__+':Follow')
>>>>>>> master
    soup = BeautifulSoup(response, "html.parser")
    follow = soup.find_all("td", "info fifty screenname")
    cursor = soup.find_all("div", "w-button-more")
    try:
        cursor = findall(r'cursor=(.*?)">', str(cursor))[0]
<<<<<<< HEAD
    except Exception as e:
        print(str(e) + " [x] feed.Follow")
=======
    except IndexError:
        logme.critical(__name__+':Follow:IndexError')
>>>>>>> master

    return follow, cursor

def Mobile(response):
<<<<<<< HEAD
    #logging.info("[<] " + str(datetime.now()) + ':: feed+Mobile')
=======
    logme.debug(__name__+':Mobile')
>>>>>>> master
    soup = BeautifulSoup(response, "html.parser")
    tweets = soup.find_all("span", "metadata")
    max_id = soup.find_all("div", "w-button-more")
    try:
        max_id = findall(r'max_id=(.*?)">', str(max_id))[0]
    except Exception as e:
<<<<<<< HEAD
        print(str(e) + " [x] feed.Mobile")
=======
        logme.critical(__name__+':Mobile:' + str(e))
>>>>>>> master

    return tweets, max_id

def profile(response):
<<<<<<< HEAD
    #logging.info("[<] " + str(datetime.now()) + ':: feed+profile')
=======
    logme.debug(__name__+':profile')
>>>>>>> master
    json_response = loads(response)
    html = json_response["items_html"]
    soup = BeautifulSoup(html, "html.parser")
    feed = soup.find_all("div", "tweet")

    return feed, feed[-1]["data-item-id"]

def Json(response):
<<<<<<< HEAD
    #logging.info("[<] " + str(datetime.now()) + ':: feed+Json')
=======
    logme.debug(__name__+':Json')
>>>>>>> master
    json_response = loads(response)
    html = json_response["items_html"]
    soup = BeautifulSoup(html, "html.parser")
    feed = soup.find_all("div", "tweet")
    return feed, json_response["min_position"]
