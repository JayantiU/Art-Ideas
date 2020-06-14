"""
This program is for building a twitter bot 
which can retweet and fav the tweets and suggest you something pretty awesome things to draw or paint
which will in turn make you creative ;).
HAPPY DRAWING!!!
"""

# Import the necessary modules... Don't forget to import our sweet tweepy ;)
import tweepy
import time
import logging
from random import choice, randint
import sqlite3
import glob
import os
from os import environ

# For logging informations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

print('this is the twitter bot')

#this is necessary to prevent other people from stealing our twitter keys
#since everything is public on github, using the environ package will solve this problem
#CONSUMER_KEY = environ['CONSUMER_KEY']
#CONSUMER_SECRET = environ['CONSUMER_SECRET']
#ACCESS_KEY = environ['ACCESS_KEY']
#ACCESS_SECRET = environ['ACCESS_SECRET']

ACCESS_KEY = "1271545311866077185-hePGq6nVkrbajpdHTG6DrnUIBPDPHH"
ACCESS_SECRET = "HUtEmjUYq56Aa3KU33FD35yuq3I6eU5MClvdTtvgnRN0P"
CONSUMER_KEY = "VvnrS1oav7i0bXiPjoPJBeRFs"
CONSUMER_SECRET = "frKD00co3t1LgDfHMGNvgMIR5bQehMLfYhH8UNlZY8WZiNB27i"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# use this object to communicate with twitter
api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)
file_name = 'recent_id.txt'

try:
    api.verify_credentials()
    logger.info("Authentication OK")
except:
    logger.error("Error during authentication", exc_info=True)

conn = sqlite3.connect('drawingIdeas.db')
c = conn.cursor()

def art_ideas(): 
    c.execute("SELECT * FROM drawingIdeas WHERE tag='Idea' AND value='Nature' ORDER BY RANDOM() LIMIT 1")
    data = c.fetchall()
    for row in data:
        idea = row[0]
    return idea

def musical_ideas(): 
    c.execute("SELECT * FROM drawingIdeas WHERE tag='Musical' ORDER BY RANDOM() LIMIT 1")
    data = c.fetchall()
    for row in data:
        idea = row[0]
    return idea

def movie_ideas(): 
    c.execute("SELECT * FROM drawingIdeas WHERE tag='Movie' ORDER BY RANDOM() LIMIT 1")
    data = c.fetchall()
    for row in data:
        idea = row[0]
    return idea

def song_ideas(): 
    c.execute("SELECT * FROM drawingIdeas WHERE tag='Song' ORDER BY RANDOM() LIMIT 1")
    data = c.fetchall()
    for row in data:
        idea = row[0]
    return idea

def book_ideas(): 
    c.execute("SELECT * FROM drawingIdeas WHERE tag='Book' ORDER BY RANDOM() LIMIT 1")
    data = c.fetchall()
    for row in data:
        idea = row[0]
    return idea

def inspo_ideas(folder): #to retrieve images stored in folder (for testing- there are 3 images in folder)
    images= glob.glob(folder + '*')
    image_open = images[randint(0,len(images))-1]
    return image_open

def retrieve_recent_id(filename):
    #Log the message information
    logger.info('Retrieving the recent Id....')
    f_read = open(filename, 'r')
    recent_id1 = int(f_read.read().strip())
    f_read.close()
    return recent_id1

def store_recent_id(recent_id, filename):
    #Log the message information
    logger.info('Storing the recent Id....')
    f_write = open(filename, 'w')
    f_write.write(str(recent_id))
    f_write.close()
    return

def reply():
    print('\nchecking')
    recent_id = retrieve_recent_id(file_name)
    mentions = api.mentions_timeline(recent_id, tweetmode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + '---' + mention.text)
        recent_id = mention.id
        store_recent_id(recent_id, file_name)

        # HELP HASHTAG
        if '#help' in mention.text.lower():
            api.update_status('@' + mention.user.screen_name +" Hello! I'm a Twitter bot that brings out your inner artist. Try tagging me with one of my hashtags for help:\n#drawings for drawing ideas\n#musicals for musical suggestions\n#songs for song recommendations\n#movies for movies to watch\n#books for literature to read", mention.id)
        # DRAWING HASHTAG
        elif '#drawings' in mention.text.lower():
            print('found you')
            theIdea = art_ideas()
            first = theIdea[0]
            # vowel formatting
            if first=="a" or first=="e" or first=="i" or first=="o" or first=="u":
                text = " Get creative! Try drawing an "
            else:
                text = " Get creative! Try drawing a "
            # s formatting
            if theIdea[-1]=="s":
                text = " Get creative! Try drawing "
            # api.update_status('@' + mention.user.screen_name + text + theIdea , mention.id)
            # PICTURE NEEDS SOME WORK OOPS
            api.update_with_media(filename="inspo_pics/birds.jpg", status=("@" + mention.user.screen_name + text + theIdea), in_reply_to_status_id=mention.id)
            # api.update_with_media(filename=inspo_ideas("inspo_pics/folder"), status=("@" + mention.user.screen_name + " HELLO WORLD"), in_reply_to_status_id=mention.id)
        # MUSICALS HASHTAG
        elif '#musicals' in mention.text.lower():
            print('found you')
            ### formatting the tweet ###
            theIdea = musical_ideas()
            api.update_status(('@' + mention.user.screen_name + " You should check out this musical: " + theIdea + "\nI hope you like it!"), mention.id)
        elif '#songs' in mention.text.lower():
            print('found you')
            ### formatting the tweet ###
            theIdea = song_ideas()
            api.update_status(('@' + mention.user.screen_name + " You should give this song a listen: " + theIdea + "\nIt's a bop!"), mention.id)
        elif '#movies' in mention.text.lower():
            print('found you')
            ### formatting the tweet ###
            theIdea = movie_ideas()
            api.update_status(('@' + mention.user.screen_name + " You should watch this movie: " + theIdea + "\nLet us know if you like it!"), mention.id)
        elif '#books' in mention.text.lower():
            print('found you')
            ### formatting the tweet ###
            theIdea = book_ideas()
            api.update_status(('@' + mention.user.screen_name + " I recommend this book: " + theIdea + "\nHope you enjoy!"), mention.id)

        # Like the tweet where it is mentioned(if not faved)
        if not mention.favorited:
            logger.info(f'Liking the tweet of {mention.user.name}')
            try:
                mention.favorite()
            except Exception as e:
                logger.error('Error while fav process .The error is :\n{}'.format(e), exc_info=True)    

        # Retweet the tweet which includes the hashtag(if not retweeted)
        if not mention.retweeted:
            logger.info(f'retweeting the tweet of {mention.user.name}')
            try:
                mention.retweet()
            except:
                logger.error('Error while retweeting.', exc_info=True)
        #Follow the user who tweeted
        try:
            mention.user.follow()
        except:
            logger.error("I don't know why this error pops up!!", exc_info=True)    

def follow_followers(api):
    #Follow them , Who follows you... We should follow... right?
    logger.info("Retrieving and following the followers")
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Following {follower.name}")
            try:
                follower.follow()
            except:
                logger.info('May be We have already followed the user or what...', exc_info=True)

while True:
    reply()
    # api.update_with_media("inspo_pics/pic.jpg", "HELLO WORLD")
    # A quick nap.... Don't wake me up for 10 sec atleast !|
    time.sleep(10)  #60 sec delay

follow_followers(api)
c.close()
conn.close()
