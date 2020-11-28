#!/usr/bin/env python3.6
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
import time
import networkx as nx
from networkx import write_graphml,read_graphml

if os.name == "posix" :
    path=os.path.expanduser("~/Desktop")
else: 
    path="."
limit=5000
userLimit=400
if (len(sys.argv) > 1):
    center= sys.argv[1]
else : 
    center= input('indica el nom de l\'usuari a buscar sense la @ inicial:')
def get_user(user):
    c = twint.Config()
    c.Username = user
    c.Store_object=True
    c.Limit=userLimit
    c.m=True
    # c.Proxy_host="tor"
    twint.output.tweets_object=[]
    users=[]
    twint.output.follows_list=users
    try: 
        twint.run.Following(c)
    except Exception as e:
        print (f'Error processant {user} amb {e}')
    if len(users)==0:
        print("no users, try again")
        time.sleep(5)
        try: 
            twint.run.Following(c)
        except Exception as e:
            print (f'Error re-processant {user} amb {e}')
    return users


def export(map,center,final):
    G = nx.DiGraph()
    users=set()
    users.add(center)
    for user,followers in map.items():
        users.add(user)
        for follower in followers:
            users.add(follower)
    for user in users:
        G.add_node( user, name= user )
        G.add_edge(user,center)
    for user,followers in map.items():
        for follower in followers:
            if follower != center:
                G.add_edge(user,follower) 
    if final:
        write_graphml(G,f"{path}/followers_following_@{center}.graphml");
    else :
        write_graphml(G,f"{path}/followers_following_@{center}_parcial.graphml");
    print("end")
        


users=[]
userMap={}

if os.path.isfile(f"{path}/followers_following_@{center}_parcial.graphml"):
    G=read_graphml( f"{path}/followers_following_@{center}_parcial.graphml")
    for s,d in G.edges:
        if d==center:
            # ara no fa res users.append(s)
            userMap[s]=[]
        else:
            userMap[s].append(d)

c = twint.Config()        
c.Username = "@"+center
c.Search = "pineapple"
c.Limit=limit
c.Format = "Tweet id: {id} | Tweet: {tweet}"
c.Store_object=True
twint.output.follows_list=users
twint.run.Followers(c)

i=0
print("number of followers:",len(users))
for user in users:
    i+=1
    if user in userMap.keys():
        continue
    time.sleep(30)
    userMap[user]=get_user(user)
    print(f'=========================={i}--{user} amb {len( userMap[user])} contactes ===============')
    if (i % 10) ==0:
        export(userMap,center,False)
export(userMap,center,True)


