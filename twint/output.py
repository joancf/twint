<<<<<<< HEAD
from . import format, get
from .tweet import Tweet
from .user import User
from datetime import datetime
from .storage import db, elasticsearch, write, panda

#import logging

_duplicate_dict = {}
follow_object = {}

tweets_object = []
user_object = []

_follow_list = []

def clean_follow_list():
    #logging.info("[<] " + str(datetime.now()) + ':: output+clean_follow_list')
    global _follow_list
    _follow_list = []

def datecheck(datestamp, config):
    #logging.info("[<] " + str(datetime.now()) + ':: output+datecheck')
    if config.Since and config.Until:
        d = int(datestamp.replace("-", ""))
        s = int(config.Since.replace("-", ""))
        if d < s:
            return False
    return True

def is_tweet(tw):
    #logging.info("[<] " + str(datetime.now()) + ':: output+is_tweet')
    try:
        tw["data-item-id"]
        return True
    except:
        return False

def _output(obj, output, config, **extra):
    #logging.info("[<] " + str(datetime.now()) + ':: output+_output')
    if config.Lowercase:
        if isinstance(obj, str):
            obj = obj.lower()
        elif str(type(obj)) == "<class 'twint.user.user'>":
            pass
        else:
            obj.username = obj.username.lower()
=======
from datetime import datetime

from . import format, get
from .tweet import Tweet
from .user import User
from .storage import db, elasticsearch, write, panda

import logging as logme

follows_list = []
tweets_list = []
users_list = []

author_list = {''}
author_list.pop()

_follows_object = {}

def clean_follow_list():
    logme.debug(__name__+':clean_follow_list')
    global _follows_object
    _follows_object = {}

def datecheck(datetimestamp, config):
    logme.debug(__name__+':datecheck')
    if config.Since and config.Until:
        logme.debug(__name__+':datecheck:dateRangeTrue')
        d = int(datetime.strptime(datetimestamp, "%Y-%m-%d %H:%M:%S").strftime('%s'))
        s = int(datetime.strptime(config.Since, "%Y-%m-%d %H:%M:%S").strftime('%s'))
        if d < s:
           return False
    logme.debug(__name__+':datecheck:dateRangeFalse')
    return True

def is_tweet(tw):
    try:
        tw["data-item-id"]
        logme.debug(__name__+':is_tweet:True')
        return True
    except:
        logme.critical(__name__+':is_tweet:False')
        return False

def _output(obj, output, config, **extra):
    logme.debug(__name__+':_output')
    if config.Lowercase:
        if isinstance(obj, str):
            logme.debug(__name__+':_output:Lowercase:username')
            obj = obj.lower()
        elif obj.__class__.__name__ == "user":
            logme.debug(__name__+':_output:Lowercase:user')
            pass
        elif obj.__class__.__name__ == "tweet":
            logme.debug(__name__+':_output:Lowercase:tweet')
            obj.username = obj.username.lower()
            author_list.update({obj.username})
>>>>>>> master
            for i in range(len(obj.mentions)):
                obj.mentions[i] = obj.mentions[i].lower()
            for i in range(len(obj.hashtags)):
                obj.hashtags[i] = obj.hashtags[i].lower()
<<<<<<< HEAD
    if config.Output != None:
        if config.Store_csv:
            try :
                write.Csv(obj, config)
            except Exception as e:
                print(str(e) + " [x] output._output")
        elif config.Store_json:
            write.Json(obj, config)
        else:
            write.Text(output, config.Output)

    if config.Pandas and obj.type == "user":
        panda.update(obj, config)
    if extra.get("follow_list"):
        follow_object.username = config.Username
        follow_object.action = config.Following*"following" + config.Followers*"followers"
        follow_object.users = _follow_list
        panda.update(follow_object, config.Essid)
    if config.Elasticsearch:
        print("", end=".", flush=True)
    else:
        if config.Store_object:
            tweets_object.append(obj)
        else:
            if not config.Hide_output:
                try:
                    print(output)
                except UnicodeEncodeError:
                    print("unicode error [x] output._output")

async def checkData(tweet, location, config, conn):
    usernames = []
    user_ids = set()
    global _duplicate_dict
    copyright = tweet.find("div", "StreamItemContent--withheld")
    if copyright is None and is_tweet(tweet):
        tweet = Tweet(tweet, location, config)

    if datecheck(tweet.datestamp, config):
        output = format.Tweet(config, tweet)

        if config.Database:
            db.tweets(conn, tweet, config)

        if config.Pandas:
            panda.update(tweet, config)

        if config.Elasticsearch:
            elasticsearch.Tweet(tweet, config)

        if config.Store_object:
            tweets_object.append(tweet) #twint.tweet.tweet

        _output(tweet, output, config)

async def Tweets(tweets, location, config, conn, url=''):
    if (config.Profile_full or config.Location) and config.Get_replies:
        for tw in tweets:
            await checkData(tw, location, config, conn)
    elif config.Favorites or config.Profile_full or config.Location:
        for tw in tweets:
            if tw['data-item-id'] == url.split('?')[0].split('/')[-1]:
                await checkData(tw, location, config, conn)
    elif config.TwitterSearch:
            await checkData(tweets, location, config, conn)
    else:
        if int(tweets["data-user-id"]) == config.User_id:
            await checkData(tweets, location, config, conn)

async def Users(u, config, conn):
    #logging.info("[<] " + str(datetime.now()) + ':: output+Users')
    global user_object
=======
            for i in range(len(obj.cashtags)):
                obj.cashtags[i] = obj.cashtags[i].lower()
        else:
            logme.info('_output:Lowercase:hiddenTweetFound')
            print("[x] Hidden tweet found, account suspended due to violation of TOS")
            return
    if config.Output != None:
        if config.Store_csv:
            try:
                write.Csv(obj, config)
                logme.debug(__name__+':_output:CSV')
            except Exception as e:
                logme.critical(__name__+':_output:CSV:Error:' + str(e))
                print(str(e) + " [x] output._output")
        elif config.Store_json:
            write.Json(obj, config)
            logme.debug(__name__+':_output:JSON')
        else:
            write.Text(output, config.Output)
            logme.debug(__name__+':_output:Text')

    if config.Pandas and obj.__class__.__name__ == "user":
        logme.debug(__name__+':_output:Pandas+user')
        panda.update(obj, config)
    if config.Elasticsearch:
        logme.debug(__name__+':_output:Elasticsearch')
        print("", end=".", flush=True)
    else:
        if not config.Hide_output:
            try:
                print(output)
            except UnicodeEncodeError:
                logme.critical(__name__+':_output:UnicodeEncodeError')
                print("unicode error [x] output._output")

async def checkData(tweet, config, conn):
    logme.debug(__name__+':checkData')
    copyright = tweet.find("div", "StreamItemContent--withheld")
    if copyright is None and is_tweet(tweet):
        tweet = Tweet(tweet, config)

        if not tweet.datestamp:
            logme.critical(__name__+':checkData:hiddenTweetFound')
            print("[x] Hidden tweet found, account suspended due to violation of TOS")
            return

        if datecheck(tweet.datestamp + " " + tweet.timestamp, config):
            output = format.Tweet(config, tweet)

            if config.Database:
                logme.debug(__name__+':checkData:Database')
                db.tweets(conn, tweet, config)

            if config.Pandas:
                logme.debug(__name__+':checkData:Pandas')
                panda.update(tweet, config)

            if config.Store_object:
                logme.debug(__name__+':checkData:Store_object')
                if hasattr(config.Store_object_tweets_list, 'append'):
                    config.Store_object_tweets_list.append(tweet)
                else:
                    tweets_list.append(tweet)

            if config.Elasticsearch:
                logme.debug(__name__+':checkData:Elasticsearch')
                elasticsearch.Tweet(tweet, config)

            _output(tweet, output, config)
    else:
        logme.critical(__name__+':checkData:copyrightedTweet')

async def Tweets(tweets, config, conn, url=''):
    logme.debug(__name__+':Tweets')
    if config.Favorites or config.Profile_full or config.Location:
        logme.debug(__name__+':Tweets:fav+full+loc')
        for tw in tweets:
            if tw['data-item-id'] == url.split('?')[0].split('/')[-1]:
                await checkData(tw, config, conn)
    elif config.TwitterSearch:
        logme.debug(__name__+':Tweets:TwitterSearch')
        await checkData(tweets, config, conn)
    else:
        logme.debug(__name__+':Tweets:else')
        if int(tweets["data-user-id"]) == config.User_id or config.Retweets:
            await checkData(tweets, config, conn)

async def Users(u, config, conn):
    logme.debug(__name__+':User')
    global users_list
>>>>>>> master

    user = User(u)
    output = format.User(config.Format, user)

    if config.Database:
<<<<<<< HEAD
        db.user(conn, config, user)

    if config.Elasticsearch:
=======
        logme.debug(__name__+':User:Database')
        db.user(conn, config, user)

    if config.Elasticsearch:
        logme.debug(__name__+':User:Elasticsearch')
>>>>>>> master
        _save_date = user.join_date
        _save_time = user.join_time
        user.join_date = str(datetime.strptime(user.join_date, "%d %b %Y")).split()[0]
        user.join_time = str(datetime.strptime(user.join_time, "%I:%M %p")).split()[1]
        elasticsearch.UserProfile(user, config)
        user.join_date = _save_date
        user.join_time = _save_time

    if config.Store_object:
<<<<<<< HEAD
        user_object.append(user) # twint.user.user
=======
        logme.debug(__name__+':User:Store_object')
        users_list.append(user) # twint.user.user
>>>>>>> master

    _output(user, output, config)

async def Username(username, config, conn):
<<<<<<< HEAD
    #logging.info("[<] " + str(datetime.now()) + ':: output+Username')
    global follow_object
    follow_var = config.Following*"following" + config.Followers*"followers"

    if config.Database:
        db.follow(conn, config.Username, config.Followers, username)

    if config.Elasticsearch:
        elasticsearch.Follow(username, config)

    if config.Store_object or config.Pandas:
        try:
            _ = follow_object[config.Username][follow_var]
        except KeyError:
            follow_object.update({config.Username: {follow_var: []}})
        follow_object[config.Username][follow_var].append(username)
        if config.Pandas_au:
            panda.update(follow_object[config.Username], config)
    _output(username, username, config, follow_list=_follow_list)
=======
    logme.debug(__name__+':Username')
    global _follows_object
    global follows_list
    follow_var = config.Following*"following" + config.Followers*"followers"

    if config.Database:
        logme.debug(__name__+':Username:Database')
        db.follow(conn, config.Username, config.Followers, username)

    if config.Elasticsearch:
        logme.debug(__name__+':Username:Elasticsearch')
        elasticsearch.Follow(username, config)

    if config.Store_object:
        follows_list.append(username)

    if config.Pandas:
        logme.debug(__name__+':Username:object+pandas')
        try:
            _ = _follows_object[config.Username][follow_var]
        except KeyError:
            _follows_object.update({config.Username: {follow_var: []}})
        _follows_object[config.Username][follow_var].append(username)
        if config.Pandas_au:
            logme.debug(__name__+':Username:object+pandas+au')
            panda.update(_follows_object[config.Username], config)
    _output(username, username, config)
>>>>>>> master
