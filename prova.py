#!/usr/bin/env python3
'''
Twint.py - Twitter Intelligence Tool (formerly known as Tweep).

See wiki on Github for in-depth details.
https://github.com/haccer/twint/wiki

Licensed under MIT License
Copyright (c) 2018 Cody Zacharias
'''

import twint
import sys
import os
limit=600
userLimit=300
center= sys.argv[1] 
def get_user(user):
    c = twint.Config()
    c.Username = user
    c.Store_object=True
    c.Limit=limit
    twint.output.tweets_object=[]
    twint.run.Following(c)
    users=twint.output.tweets_object
    return users    

def export(map,center):
    f = open("/home/joan/Desktop/SNA/data/twitter/ego/followers_"+center+".gdf","wt",encoding="utf8")
    users=set()
    users.add(center)
    for user,followers in map.items():
        users.add(user)
        for follower in followers:
            users.add(follower)
    f.write("nodedef>name VARCHAR,label VARCHAR,type VARCHAR \n")
    for user in users:
        f.write("@{},@{},user \n".format(user,user))
    f.write("edgedef>node1 VARCHAR,node2 VARCHAR, weight DOUBLE,directed BOOLEAN, label VARCHAR \n")
    for user,followers in map.items():
        f.write("@{},@{},1.0,true,follow \n".format(user,center))
        for follower in followers:
            if follower != center:
                f.write("@{},@{},1.0,true,follow \n".format(user,follower)  )  
    f.close()
    print("end")
        
c = twint.Config()

c.Username = center
c.Search = "pineapple"
c.Limit=limit
c.Format = "Tweet id: {id} | Tweet: {tweet}"
c.Store_object=True

# Run
twint.run.Followers(c)
users=twint.output.tweets_object
userMap={}
i=0
print("number of followers:",len(users))
for user in users:
    userMap[user]=get_user(user)
    i+=1
    print(i,user,len( userMap[user]))
export(userMap,center)


