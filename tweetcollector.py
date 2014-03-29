#!/usr/bin/env python
# -*- coding: utf-8  -*-
#encoding=utf-8

# import lib.tweepy as tweepy
import tweepy
import time
import os
import json
from stemming import porter2
import re

def tokenize(text):
    """
    Take a string and split it into tokens on word boundaries.
      
    A token is defined to be one or more alphanumeric characters,
    underscores, or apostrophes.  Remove all other punctuation, whitespace, and
    empty tokens.  Do case-folding to make everything lowercase. This function
    should return a list of the tokens in the input string.
    """
    tokens = re.findall("[\w']+", text.lower())
    return [porter2.stem(token) for token in tokens]

class TwitterCrawler():
    # Fill in the blanks here for your own Twitter app.
    # consumer_key = ""
    # consumer_secret = ""
    # access_key = ""
    # access_secret = ""

    # My Key
    consumer_key = 'KW3eLVXHPBNueZJZOIQ'
    consumer_secret = '4nMJhuPxhMXbAM0QfXHF56SaPPNYjbR24zdCv078Q'
    access_key = '2416454197-RJtHf7L2nHbs4Nqi3U186iFOa6YaFeatEe450M0'
    access_secret = 'KpDXMptCpyhq6mmgXAoiyQEjyhEgnwnJSDy59t5jdBtcj'
    
    auth = None
    api = None

    username = "soccerfan1392"

    def __init__(self):
        self.username = 'soccerfan1392'
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(self.auth)
        # print self.api.rate_limit_status()

    def re_init(self, access_key, access_secret, username):
        self.access_key = access_key
        self.access_secret = access_secret
        self.username = username
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(self.auth)
        
    def setUsername(self, username):
        self.username = username

    def setKeys(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_key, self.access_secret)
        self.api = tweepy.API(self.auth)

    def check_api_rate_limit(self, sleep_time):
        try:
            rate_limit_status = self.api.rate_limit_status()
            # if rate_limit_status['resources']['statuses']['/statuses/user_timeline']['remaining'] < 10:
            #     print "Sleeping for %d seconds." %(sleep_time)
            #     print rate_limit_status['resources']['statuses']
            #     time.sleep(sleep_time)
            #     rate_limit_status = self.api.rate_limit_status()
            print rate_limit_status['resources']['statuses']['/statuses/user_timeline']
        except Exception as error_message:
            if error_message is "[{u'message': u'Over capacity', u'code': 130}]" :
                print "True for string checking"
                # print "Sleeping for %d seconds." %(sleep_time)
                # print rate_limit_status['resources']['statuses']
                time.sleep(sleep_time)
                print rate_limit_status['resources']['statuses']['/statuses/user_timeline']
            # if error_message['code'] == 130:
            #     print 'True for code checking '

    def collect_tweets(self, queryList):
        tw = {}
        tweetList = []
        stopper = 0
        docText = ""
        printList = []
        for query in queryList:
            for tweet in tweepy.Cursor(self.api.search,
                q=query,
                rpp=100,
                result_type="recent",
                include_entities=True,
                lang="en").items(20):
                # docText = tweet.text.encode('utf-8')
                # printList.append(docText)
                printList.append(get_attributes(tweet))

        #Print to file for testing purposes
        # fileName = docName + ".json"
        # with open(fileName, 'w') as outfile:
        #     for tweet in printList:
        #         json.dump(tweet, outfile)
        #         outfile.write('\n')
            # json.dump(printList, outfile)

        # return (docName, printList) 
        return printList  

    def getTweetsText(self, tweets):
        doc = []
        for tweet in tweets:
            text = tweet['text']
            text_tokenized = tokenize(text)
            for word in text_tokenized:
                doc.append(word)
        return ' '.join(doc)

    def getTweetID(self, tweets):
        id_list = []
        for tweet in tweets:
            id_list.append(tweet['id_str'])
        return ' '.join(id_list)

    def get_query_result(self, query):
        tweets = tweepy.Cursor(self.api.search, q = query, count = 20, result_type = "recent", include_entities = True, lang = "en").items(20)
        result = []
        for tweet in tweets:
            result_dict = {}
            text = tweet.text.encode('utf-8', 'ignore')
            id_str = tweet.id_str
            result_dict.setdefault('text', text)
            result_dict.setdefault('id_str', id_str)
            result.append(result_dict)
        return result

    # Return text in UTF8 and ignore illegal characters in UTF8
    def get_encoded_text(self, text):
        return text.encode('UTF-8', 'ignore')

    # Returns the authenticated user’s information.
    def get_me(self):
        return self.api.me()

    # Returns the user by either ID or screen name 
    def get_user(self, screen_name):
        return self.api.get_user(screen_name)

    # Return 20 of the most recent tweets given the user's ID or screen name 
    def get_user_timeline(self, user):
        c = user.statuses_count if user.statuses_count < 50 else 50
        return self.api.user_timeline(user.screen_name, count = c)
        # return self.api.user_timeline(screen_name)

    # Return friends of the user 
    def get_friends_name(self, user):
        c = user.friends_count if user.friends_count < 20 else 20
        return [dict(get_attributes(friend)) for friend in user.friends(count = c)]
        # for friend in user.friends(count = c):
        #     yield friend.screen_name


    # Return a Twitter User with info of username and tweets
    def get_twitter_user(self, user):
        # Get the authenticated user info  
        username = user.screen_name

        recent_status = self.get_user_timeline(user)
        tu = TwitterUser(dict(get_attributes(user)))
        tu.add_tweets(recent_status)
        return tu

    # Return a twitter user with self tweets, friends and friends' tweets
    def get_twitter_user_with_friends(self):
        # user = self.get_user(username)
        # user = self.get_me()
        user = self.get_user(self.username)
        # print user.statuses_count
        # print user.profile_image_url_https

        twitter_user = self.get_twitter_user(user)
        friends_list = self.get_friends_name(user)
        twitter_user.set_friends_name(friends_list)

        # Add friends user into TwitterUser
        # for friend_name in friends_list:
            # friend_user = self.get_user(friend_name)
            # fu = self.get_twitter_user(friend_user)
            # twitter_user.add_friend(fu)

        return twitter_user

    # return a friend user with tweets 
    def get_user_friend(self, friendname):
        user = self.get_user(friendname)
        twitter_user = self.get_twitter_user(user)

        return twitter_user

# Return a list of all attributes associate with the object
def get_attributes(obj):
    return dict(obj.__getstate__())
    # return obj.json

def get_json(obj):
    return obj.json

# ------------- Overload json.dumps to fix the problem --------------------
@classmethod                    
def parse(cls, api, raw):
        status = cls.first_parse(api, raw)
        setattr(status, 'json', json.dumps(raw))
        return status

tweepy.Status.first_parse = tweepy.Status.parse
tweepy.Status.parse = parse
# ------------- Overload json.dumps to fix the problem --------------------

class TwitterUser():
    """docstring for TwitterUser"""
    def __init__(self, userinfo):
        # user's screen name 
        self.userinfo = userinfo
        # a list of tweet in dictionary data structure
        self.mytweets = []
        # a list of friends in TwitterUser data structure 
        self.friends = []
        self.friend_users = []

        # debug 
        self.tweets_json = []

    def add_tweets(self, tweets):
        for tweet in tweets:
            self.mytweets.append(get_attributes(tweet))
            self.tweets_json.append(get_json(tweet))

    def add_friend(self, friend_user):
        self.friend_users.append(friend_user)

    # Save friends' name
    def set_friends_name(self, friends_list):
        self.friends = friends_list

    def __tojson__(self):
        return str(self.username) + '\'s Timeline: ' + '\n'.join([str(tweet) for tweet in self.mytweets]) 

        # if self.friend_users:
        #     for user in self.friend_users:
        #         user.__tojson__()

        # '\n'.join([user.__tojson__() for user in self.friend_users])

    def write_data(self):
        with open(os.path.join(os.getcwd(), self.username + '.json'), 'w') as f:
            output_title = dict()
            output_title['username'] = self.username
            output_title['friends_name'] = self.friends_name
            json.dump(output_title, f)
            f.write('\n')
            for tweet in self.tweets_json:
                d = json.loads(tweet)
                json.dump(d, f)
                f.write('\n')

            # for user in self.friend_users:
            #     for friend_tweet in user.mytweets:
            #         d = json.loads(friend_tweet)
            #         json.dump(d, f)
            #         f.write('\n')

    # debug
    def printdata(self):
        for tweet in self.mytweets:
            print tweet

def write_data(filename, tweets_json):
    with open(os.path.join(os.getcwd(), filename + '.json'), 'w') as f:
        for tweet in tweets_json:
            d = json.loads(tweet)
            json.dump(d, f)
            f.write('\n')

def read_data(filename):
    tweets = [] 
    with open(os.path.join(os.getcwd(), filename + '.json'), 'r') as f: 
        for line in f: 
            t = json.loads(line)
            tweets.append(t)
    return tweets

def main():
    querylist = ['from:marchmadness']
    tc = TwitterCrawler()
    tc.check_api_rate_limit(900)
    result = tc.collect_tweets(querylist)
    write_data('marchmadness', result)

    tc.check_api_rate_limit(900)

    result = read_data('marchmadness')
    print result

if __name__ == "__main__":
    main()
