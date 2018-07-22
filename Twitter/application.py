
import sys
sys.path.insert(0, '/application')
from flask import Flask, render_template, request
import re
import csv
import time
import sys
# import matplotlib.pyplot as plt
import pickle
import json
from datetime import date
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import re
import cgi

# import matplotlib.pyplot as mat
from tweepy import OAuthHandler
#import plotly.plotly as py
#import plotly.graph_objs as go
from neo4j.v1 import GraphDatabase
import json
import webbrowser
#from flask_sqlalchemy import SQLAlchemy
import os
import datetime
import subprocess
import nltk

from nltk.corpus import stopwords, state_union
from nltk.tokenize import word_tokenize, sent_tokenize
import tweepy
import json
from textblob import TextBlob
from flask import Flask,request,render_template
punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''


with open("stopwords.txt","r") as sp:
    stopWords=pickle.load(sp)
from py2neo import Graph, Node, Relationship
graph = Graph("http://18.207.142.251:34337/browser/", password="wheel-belt-town")
graph.run("MATCH(n)"
          "DETACH DELETE (n)")
#graph.run("using Periodic commit")
def perc(part, whole):
    return 100 * (float(part) / float(whole))


def get_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# Elastic Beanstalk initalization
application = Flask(__name__)
#application.debug=True
# change this to your own value
#application.secret_key = 'cC1YCIWOj9GgWspgNEo2'   

@application.route('/', methods=['GET', 'POST'])
def ser():
    return render_template('home.html')


@application.route('/search', methods=['GET', 'POST'])
def wait():

    s= request.form['search']
    sd= request.form['sd']
    sm= request.form['sm']
    sy= request.form['sy']
    ed= request.form['ed']
    em = request.form['sm']
    ey = request.form['sy']
    m = request.form['m']

    consumer_key = 'orTqJZU3cMu2Rbvs53Cehkw83'
    consumer_secret = '99LyoXWUCM9NMC2myQprhtaMeJQfr8ViVJHv90VxPPzYrh3iE1'
    access_token = '957488729878233089-q8SjiOedlzN4Snvujycouz06Q0dPnqe'
    access_token_secret = 'amdxwanGMBOw9GhxR7tey3uCighozovybhuhfAAmIQkSz'
    graph.run("MERGE (pos:Category{type:'Positive'})")
    graph.run("MERGE (pos:Category{type:'Negative'})")
    graph.run("MERGE (pos:Category{type:'Neutral'})")
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    npos = nneg = nnut = ntweets = 0
    #render_template('wait.html')
    

    # sd,sm,sy=raw_input("enter start datetime in format %d-%m-%y").split("-")
    # ed,em,ey=raw_input("enter end datetime in format %d-%m-%y").split("-")
    startDate = datetime.datetime(int(sy), int(sm), int(sd), 23, 59, 59)
    endDate = datetime.datetime(int(ey), int(em), int(ed), 23, 59, 59)
    # search=raw_input("enter the query or hashtag to search\t:")
    #print(startDate)
    #print(endDate)
    n=0
    for tweet in tweepy.Cursor(api.search, q=s, lang="en").items(int(m)):
            n+=1
            if n>m:
                break
            if (tweet.created_at < endDate and tweet.created_at > startDate):
                #data = {}
                #data['tno'] = int(ntweets + 1)
                # data['date']=tweet.created_at
                #data['text'] = tweet.text
                #print(tweet.created_at, tweet.text)
                #print("\n\n\n")
                words = tweet.text.split()
                
                #for u in words:
                #	u=u.lower()

                #data['words'] = words
                if (get_sentiment(tweet.text) == "positive"):
                    #data['sno'] = int(npos)
                    #data['cat'] = "pos"
                    #with open("postweets.json", "a") as fp:
                     #   json.dump(data, fp, indent=2, encoding='utf8')
                    posnode = Node("tweet", text=tweet.text, sno=npos, tno=ntweets, cat="pos", words=words)
                    words = tweet.text.split()
                    #words = [w for w in words if not w in stopwords]
                    graph.create(posnode)
                    for w in words:
                        if w not in stopWords and w not in punctuations:
                            #print(w)
                            w_token = Node("word", token=w, tno=ntweets)
                            graph.create(w_token)
                    npos += 1;
                elif (get_sentiment(tweet.text) == "negative"):
                    #data['sno'] = int(npos)
                    #data['cat'] = "neg"
                    #with open("negtweets.json", "a") as fp:
                     #   json.dump(data, fp, indent=2)
                    negnode = Node("tweet", text=tweet.text, sno=npos, tno=ntweets, cat="neg", words=words)
                    graph.create(negnode)
                    words = tweet.text.split()
                    for w in words:
                        if w not in stopWords and w not in punctuations:
                            #print(w)
                            w_token = Node("word", token=w, tno=ntweets)
                            graph.create(w_token)
                    nneg += 1;
                else:
                    #data['sno'] = int(npos)
                    #data['cat'] = "nut"
                    #with open("nuttweets.json", "a") as fp:
                    #    json.dump(data, fp, indent=2)
                    nutnode = Node("tweet", text=tweet.text, sno=npos, tno=ntweets, cat="nut", words=words)
                    graph.create(nutnode)
                    words = tweet.text.split()
                    for w in words:
                        if w not in stopWords and w not in punctuations:
                            #print(w)
                            w_token = Node("word", token=w, tno=ntweets)
                            graph.create(w_token)
                    nnut += 1;
            
                #print(tweet.created_at, tweet.text)
                #print("\nOUT OF DATE RANGE\n\n\n")
            	ntweets += 1
        #print(ntweets)
    
    
    graph.run("match (w:word),(t:tweet) "
              "where w.tno=t.tno "
              "create (t)-[:has]->(w) ")

    graph.run("match (cat:Category{type:'Positive'}) "
              "match (t:tweet{cat:'pos'})"
              "merge (t)-[:is]->(cat)")

    graph.run("match (cat:Category{type:'Negative'}) "
              "match (t:tweet{cat:'neg'})"
              "merge (t)-[:is]->(cat)")

    graph.run("match (cat:Category{type:'Neutral'}) "
              "match (t:tweet{cat:'nut'})"
              "merge (t)-[:is]->(cat)")
    
    posperc = perc(npos, ntweets)
    negperc = perc(nneg, ntweets)
    nutperc = perc(nnut, ntweets)
    #print(" no of positive tweets : " + str(npos) + " percentage: " + str(posperc))
    #print(" no of negative tweets : " + str(nneg) + " percentage: " + str(negperc))
    #print(" no of neutral  tweets : " + str(nnut) + " percentage: " + str(nutperc))
    # graph.open_browser( graph.run("match(n) return(n)"))
    #with open("/Users/Harshithsheshan/Desktop/output.json", "w") as jp:
    #   for i in graph.run("MATCH (n) RETURN(n)"):
    #      json.dump(i,jp,indent=2)
    return render_template('result.html',ntweets=ntweets,npos=npos,nneg=nneg,nnut=nnut,posperc=posperc,negperc=negperc,nutperc=nutperc)
                   
if __name__ == '__main__':
    application.run()
