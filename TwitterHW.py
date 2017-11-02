#name: ILma Bilic
#date: 11/2/17
#comments: Had to use uprint

# Import statements
import unittest
import sqlite3
import requests
import json
import re
import tweepy
import twitter_info # still need this in the same directory, filled out

consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and return it in a JSON format
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

import sys
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

# And we've provided the setup for your cache. But we haven't written any functions for you, so you have to be sure that any function that gets data from the internet relies on caching.
CACHE_FNAME = "twitter_cache.json"
try:
    cache_file = open(CACHE_FNAME,'r')
    cache_contents = cache_file.read()
    cache_file.close()
    CACHE_DICTION = json.loads(cache_contents)
except:
    CACHE_DICTION = {}

## [PART 1]

# Here, define a function called get_tweets that searches for all tweets referring to or by "umsi"
# Your function must cache data it retrieves and rely on a cache file!


def get_tweets(word):

    full_search = "twitter_{}".format(word)
    # api = tweepy.API(auth)
    # full_search = api.user_timeline(screen_name = 'UMSI', count = 20, include_rts = True)
    # for status in full_search:
    #     print (status.author, status.user)
    if full_search in CACHE_DICTION:
        uprint("Data was in the cache")
        uprint("\n")
        return CACHE_DICTION[full_search] #send word to loop to retreive text
    else:
        uprint("Making a request for new data...")
        results = api.search(q = full_search)
        try:
            CACHE_DICTION[full_search] = results
            dumped_json_cache = json.dumps(CACHE_DICTION)
            fw = open(CACHE_FNAME,"w")
            fw.write(dumped_json_cache)
            fw.close() # Close the open file
            return CACHE_DICTION[full_search]
        except:
            uprint("Wasn't in cache and wasn't valid search either")
            return None



# api = tweepy.API(auth)
# data = api.user_timeline(screen_name = 'UMSI', count = 20, include_rts = True)
# for status in data:
#     print (status.author, status.user)

## [PART 2]
# Create a database: tweets.sqlite,
# And then load all of those tweets you got from Twitter into a database table called Tweets, with the following columns in each row:
## tweet_id - containing the unique id that belongs to each tweet
## author - containing the screen name of the user who posted the tweet (note that even for RT'd tweets, it will be the person whose timeline it is)
## time_posted - containing the date/time value that represents when the tweet was posted (note that this should be a TIMESTAMP column data type!)
## tweet_text - containing the text that goes with that tweet
## retweets - containing the number that represents how many times the tweet has been retweeted

# Below we have provided interim outline suggestions for what to do, sequentially, in comments.
#
# # 1 - Make a connection to a new database tweets.sqlite, and create a variable to hold the database cursor.
conn = sqlite3.connect('tweets.sqlite')
cur = conn.cursor()
#
#
# # 2 - Write code to drop the Tweets table if it exists, and create the table (so you can run the program over and over), with the correct (4) column names and appropriate types for each.
# # HINT: Remember that the time_posted column should be the TIMESTAMP data type!
# cur.execute('DROP TABLE IF EXISTS Tweets')
# cur.execute('CREATE TABLE Tweets (tweet_id TEXT, author TEXT, time_posted TIMESTAMP, tweet_text TEXT, retweets NUMBER)')
# # 3 - Invoke the function you defined above to get a list that represents a bunch of tweets from the UMSI timeline. Save those tweets in a variable called umsi_tweets.
# umsi_tweets = get_tweets()

umsi_tweets = get_tweets('umsi')

    #  data = tweet["text"]
    #  uprint ('TEXT: ' + data)
    #  date = tweet["created_at"]
    #  uprint ('CREATED AT: ' + date)
    #  user = tweet['user']['screen_name']
    #  uprint ('User: ' + user)
    #  uprint("\n")
# # 4 - Use a for loop, the cursor you defined above to execute INSERT statements, that insert the data from each of the tweets in umsi_tweets into the correct columns in each row of the Tweets database table.

text = (umsi_tweets['statuses'])
for tweet in text:
    tup = tweet['id'],tweet['user']['screen_name'], tweet['created_at'], tweet['text'], tweet['retweet_count']
    cur.execute('INSERT INTO Tweets(tweet_id, author, time_posted, tweet_text, retweets) VALUES (?,?,?,?,?)', tup)


# #  5- Use the database connection to commit the changes to the database
conn.commit() #needed to insert data
# # You can check out whether it worked in the SQLite browser! (And with the tests.)
# print ('test for part 2')
# cur.execute('SELECT time_posted, tweet_text FROM Tweets')
# all_res = cur.fetchall()
# for t in all_res:
    # print(t[0] + " - " + t[1] + "\n")
#
# ## [PART 3] - SQL statements
# # Select all of the tweets (the full rows/tuples of information) from umsi_tweets and display the date and message of each tweet in the form:
#     # Mon Oct 09 16:02:03 +0000 2017 - #MondayMotivation https://t.co/vLbZpH390b
#     #
#     # Mon Oct 09 15:45:45 +0000 2017 - RT @MikeRothCom: Beautiful morning at @UMich - It’s easy to forget to
#     # take in the view while running from place to place @umichDLHS  @umich…
# # Include the blank line between each tweet.
cur.execute('SELECT time_posted, tweet_text FROM Tweets')
date_message = cur.fetchall()
for tw in date_message:
    uprint(tw[0] + " - " + tw[1] + "\n")
# cur.close()
# # Select the author of all of the tweets (the full rows/tuples of information) that have been retweeted MORE
# # than 2 times, and fetch them into the variable more_than_2_rts.
# # Print the results
cur.execute("SELECT author FROM Tweets WHERE retweets > 2")
more_than_2_rts = cur.fetchall()
print ('more_than_2_rts = %s' % set(more_than_2_rts))


if __name__ == "__main__":
    unittest.main(verbosity=2)
