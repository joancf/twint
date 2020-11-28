#!/usr/bin/env python3.6
'''
Twint.py - Twitter Intelligence Tool (formerly known as Tweep).

See wiki on Github for in-depth details.
https://github.com/haccer/twint/wiki

Licensed under MIT License
Copyright (c) 2018 Cody Zacharias
'''
import sys
import os
import twint
import re
import unicodedata
import pickle
import traceback



limit=5000
userLimit=300
center= "#"+sys.argv[1]
def get_user(user):
    c = twint.Config()
    c.Username = user
    c.Store_object=True
    c.Limit=userLimit
    c.m=True
    c.Proxy_host="tor"
    twint.output.tweets_object=[]
    users=[]
    twint.output.follows_list=users
    twint.run.Following(c)
    return users

def export(tweets,map,center):
    f = open("../ego/Hashfollowers_"+center+"2.gdf","wt",encoding="utf8")
    users={}
    tweetsMap=set()
    # PREPARE THE NODES
    for user,followers in map.items():
        users[user]=[]
        for follower in followers:
            try:
                users[follower.username.lower()]=follower.followers
            except:
                users[follower]=[]
    f.write("nodedef>name VARCHAR,label VARCHAR,type VARCHAR,replies INT, tweet VARCHAR  \n")
    for user in users:
        f.write("@{},@{},user,, \n".format(user,user))
    t=0
    w=0
    wordset=set()
    for tweet in tweets:
        t+=1
        if tweet.id not in tweetsMap:
            w+=1
            if (not tweet.retweet) :
                text=" ".join(tweet.tweet.replace("['\"\n,]",' ').splitlines())
                f.write("{},{},tweet,{},'{}'\n".format(tweet.id, tweet.id,tweet.retweets_count, text))
                words=text.split();
                for word in words:
                	normal = unicodedata.normalize( 'NFKD', word ).encode( 'ASCII', 'ignore' ).decode( 'utf-8' ).lower()
                	normalized = re.sub( '[^\w#@]', '', normal )
                	if len(normalized) >2:
                    		wordset.add(normalized)
            tweetsMap.add(tweet.id)
        else :
            print("tweet already there {}".format(tweet.tweet))
    for word in wordset:	
       	f.write("{},{},word,, \n".format(word, word))
    print("written {} from a total of {}".format(w,t))
    f.write("edgedef>node1 VARCHAR,node2 VARCHAR, weight DOUBLE,directed BOOLEAN, label VARCHAR \n")
    for user,followers in map.items():
        for follower in followers:
            if isinstance(follower, str):
                follName=follower
            else :
                follName = follower.username.lower()
            if follName != user:
                f.write("@{},@{},1.0,true,follow \n".format(user.lower(),follName)  )
    for tweet in tweets:
            if tweet.id in tweetsMap:
                if (not tweet.retweet) :
                    f.write("@{},{},1.0,true,author \n".format(tweet.username,tweet.id))
                    words=(" ".join(tweet.tweet.replace("['\"\n,]",' ').splitlines())).split();
                    for word in words:
                    	normal = unicodedata.normalize( 'NFKD', word ).encode( 'ASCII', 'ignore' ).decode( 'utf-8' ).lower()
                    	normalized = re.sub( '[^\w#@]', '', normal )
                    	if len(normalized) >2:
                    		if normalized[0]=="@":
                    			f.write("{},{},1.0,true,mention \n".format(tweet.id, normalized))
                    		else:
                    	    		f.write("{},{},1.0,true,word \n".format(tweet.id, normalized))
                else:   # if it's a retweet
                    f.write("@{},{},1.0,true,retweet \n".format(tweet.username,tweet.id))
    f.close()
    print("end")
        
c = twint.Config()

c.Search = center
c.Limit=limit
c.Format = "Tweet id: {id} | Tweet: {tweet} | Username: {username}"
c.Proxy_host="tor"
c.Store_object=True
follow=False
if (len(sys.argv)==3) and (sys.argv[2]=="load") :
    follow=True
    tweetsf = open( 'data/'+center+"tweetsF", 'rb' )
    tweets=pickle.load(tweetsf)
    tweetsf.close()
    userMf = open( 'data/'+center+"usersMapF", 'rb' )
    userMap=pickle.load(userMf)
    userMf.close()
else:
    # Run
    twint.run.Search(c)
    tweets=twint.output.tweets_list
    tweetsf = open( 'data/'+center+"tweetsF", 'wb' )
    pickle.dump(tweets,tweetsf)
    tweetsf.close()
    userMap={}

i=0
j=0
u=0
print("number of tweets:",len(tweets))
tweetsMap=set()
try:
    for tweet in tweets:
        if tweet.id not in tweetsMap:
             tweetsMap.add(tweet.id)
             print( "tweet from user  {}   ".format(   tweet.username )  )
             if not (follow or tweet.username in userMap):
                 u += 1
                 userMap[tweet.username.lower()] = get_user( tweet.username.lower() )
                 print( "{} user  {}  following {}".format( u, tweet.username, len( userMap[tweet.username] ) ) )
                 if u % 10 == 0:
                     print( "Saving to dump" )
                     usersMf = open( 'data/'+center + "usersMapF", 'wb' )
                     pickle.dump(  userMap,usersMf )
                     usersMf.close()
             else:
                 print( 'skip user  {}   '.format( tweet.username ) )

             j+=1
        else:
            print("this is a retweet")
        if not tweet.retweets_count == '0':
            print ("number of retweets " + tweet.retweets_count)

        i+=1
        print("processing {} differents {}".format(i,j))
except :
    traceback.print_exc()
    pass
print( "exporting" )
export(tweets,userMap,center)



