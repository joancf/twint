from time import strftime, localtime
<<<<<<< HEAD
import json
#from datetime import datetime
#import logging
=======
from datetime import datetime
import json

import logging as logme
>>>>>>> master

class tweet:
    """Define Tweet class
    """
    type = "tweet"

    def __init__(self):
        pass

def getMentions(tw):
<<<<<<< HEAD
    #logging.info("[<] " + str(datetime.now()) + ':: tweet+getMentions')
    """Extract ment from tweet
    """
    try:
        mentions = tw["data-mentions"].split(" ")
    except:
        mentions = ""
=======
    """Extract ment from tweet
    """
    logme.debug(__name__+':getMentions')
    try:
        mentions = tw["data-mentions"].split(" ")
    except:
        mentions = []
>>>>>>> master

    return mentions

def getQuoteURL(tw):
<<<<<<< HEAD
    #logging.info("[<] " + str(datetime.now()) + ':: tweet+getQuoteInfo')
    """Extract quote from tweet
    """
=======
    """Extract quote from tweet
    """
    logme.debug(__name__+':getQuoteURL')
>>>>>>> master
    base_twitter = "https://twitter.com"
    quote_url = ""
    try:
        quote = tw.find("div","QuoteTweet-innerContainer")
        quote_url = base_twitter + quote.get("href")
    except:
        quote_url = ""

    return quote_url

def getText(tw):
<<<<<<< HEAD
    #logging.info("[<] " + str(datetime.now()) + ':: tweet+getText')
    """Replace some text
    """
    text = tw.find("p", "tweet-text").text
    text = text.replace("\n", " ")
=======
    """Replace some text
    """
    logme.debug(__name__+':getText')
    text = tw.find("p", "tweet-text").text
>>>>>>> master
    text = text.replace("http", " http")
    text = text.replace("pic.twitter", " pic.twitter")

    return text

def getStat(tw, _type):
    """Get stats about Tweet
    """
<<<<<<< HEAD
    #logging.info("[<] " + str(datetime.now()) + ':: tweet+getStat')
    st = f"ProfileTweet-action--{_type} u-hiddenVisually"
    return tw.find("span", st).find("span")["data-tweet-stat-count"]

def getRetweet(profile, username, user):
    #logging.info("[<] " + str(datetime.now()) + ':: tweet+getRetweet')
    if profile and username.lower() != user.lower():
        return 1

def Tweet(tw, location, config):
    """Create Tweet object
    """
    ##logging.info("[<] " + str(datetime.now()) + ':: tweet+Tweet')
=======
    logme.debug(__name__+':getStat')
    st = f"ProfileTweet-action--{_type} u-hiddenVisually"
    return tw.find("span", st).find("span")["data-tweet-stat-count"]

def getRetweet(tw):
    """Get Retweet
    """
    logme.debug(__name__+':getRetweet')
    _rt_object = tw.find('span', 'js-retweet-text')
    if _rt_object:
        _rt_id = _rt_object.find('a')['data-user-id']
        _rt_username = _rt_object.find('a')['href'][1:]
        return  _rt_id, _rt_username
    return '', ''

def Tweet(tw, config):
    """Create Tweet object
    """
    logme.debug(__name__+':Tweet')
>>>>>>> master
    t = tweet()
    t.id = int(tw["data-item-id"])
    t.id_str = tw["data-item-id"]
    t.conversation_id = tw["data-conversation-id"]
    t.datetime = int(tw.find("span", "_timestamp")["data-time-ms"])
    t.datestamp = strftime("%Y-%m-%d", localtime(t.datetime/1000.0))
    t.timestamp = strftime("%H:%M:%S", localtime(t.datetime/1000.0))
    t.user_id = int(tw["data-user-id"])
    t.user_id_str = tw["data-user-id"]
    t.username = tw["data-screen-name"]
    t.name = tw["data-name"]
<<<<<<< HEAD
    t.profile_image_url = tw.find("img", "js-action-profile-avatar").get('src').replace("_bigger","")
    t.place = tw.find("a","js-geo-pivot-link").text.strip() if tw.find("a","js-geo-pivot-link") else None
=======
    t.place = tw.find("a","js-geo-pivot-link").text.strip() if tw.find("a","js-geo-pivot-link") else ""
>>>>>>> master
    t.timezone = strftime("%Z", localtime())
    for img in tw.findAll("img", "Emoji Emoji--forText"):
        img.replaceWith(img["alt"])
    t.mentions = getMentions(tw)
    t.urls = [link.attrs["data-expanded-url"] for link in tw.find_all('a',{'class':'twitter-timeline-link'}) if link.has_attr("data-expanded-url")]
    t.photos = [photo_node.attrs['data-image-url'] for photo_node in tw.find_all("div", "AdaptiveMedia-photoContainer")]
<<<<<<< HEAD
    t.tweet = getText(tw)
    t.location = location
    t.hashtags = [hashtag.text for hashtag in tw.find_all("a","twitter-hashtag")]
=======
    t.video = 1 if tw.find_all("div", "AdaptiveMedia-video") != [] else 0
    t.tweet = getText(tw)
    t.hashtags = [hashtag.text for hashtag in tw.find_all("a","twitter-hashtag")]
    t.cashtags = [cashtag.text for cashtag in tw.find_all("a", "twitter-cashtag")]
>>>>>>> master
    t.replies_count = getStat(tw, "reply")
    t.retweets_count = getStat(tw, "retweet")
    t.likes_count = getStat(tw, "favorite")
    t.link = f"https://twitter.com/{t.username}/status/{t.id}"
<<<<<<< HEAD
    t.retweet = getRetweet(config.Profile, t.username, config.Username)
    t.quote_url = getQuoteURL(tw)
=======
    t.user_rt_id, t.user_rt = getRetweet(tw)
    t.retweet = True if t.user_rt else False
    t.retweet_id = tw['data-retweet-id'] if t.user_rt else ''
    t.retweet_date = datetime.fromtimestamp(((t.id >> 22) + 1288834974657)/1000.0).strftime("%Y-%m-%d %H:%M:%S") if t.user_rt else ''
    t.quote_url = getQuoteURL(tw)
    t.near = config.Near if config.Near else ""
    t.geo = config.Geo if config.Geo else ""
    t.source = config.Source if config.Source else ""
    t.reply_to = [{'user_id': t['id_str'], 'username': t['screen_name']} for t in json.loads(tw["data-reply-to-users-json"])]
>>>>>>> master
    return t
