import tweepy
import time
from random import choice


print('this is the twitter bot')

CONSUMER_KEY = 'VvnrS1oav7i0bXiPjoPJBeRFs'
CONSUMER_SECRET = 'frKD00co3t1LgDfHMGNvgMIR5bQehMLfYhH8UNlZY8WZiNB27i'
ACCESS_KEY = '1271545311866077185-hePGq6nVkrbajpdHTG6DrnUIBPDPHH'
ACCESS_SECRET = 'HUtEmjUYq56Aa3KU33FD35yuq3I6eU5MClvdTtvgnRN0P'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth) #use this object to communicate with twitter

file_name = 'recent_id.txt'

def art_ideas(): #replace with goolge cloud potientially?
    ideas = ['pencil', 'book', 'pillow', 'towel']
    return choice(ideas)

def retrieve_recent_id(filename):
    f_read = open(filename, 'r')
    recent_id1= int(f_read.read().strip())
    f_read.close()
    return recent_id1

def store_recent_id(recent_id, filename):
    f_write = open(filename,'w')
    f_write.write(str(recent_id))
    f_write.close()
    return

def reply():
    print('checking')
    recent_id = retrieve_recent_id(file_name)
    mentions = api.mentions_timeline(recent_id, tweetmode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + '---' + mention.text)
        recent_id = mention.id
        store_recent_id(recent_id,file_name)
        if'#whatshouldidraw' in mention.text.lower():
            print('found you')
            api.update_status('@' + mention.user.screen_name + 'Here, you can draw a ' + art_ideas() , mention.id)


while True:
    reply()
    time.sleep(2) #10 sec delay
