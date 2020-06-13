import tweepy
import time
from random import choice, randint
import sqlite3
import glob

print('this is the twitter bot')

CONSUMER_KEY = 'VvnrS1oav7i0bXiPjoPJBeRFs'
CONSUMER_SECRET = 'frKD00co3t1LgDfHMGNvgMIR5bQehMLfYhH8UNlZY8WZiNB27i'
ACCESS_KEY = '1271545311866077185-hePGq6nVkrbajpdHTG6DrnUIBPDPHH'
ACCESS_SECRET = 'HUtEmjUYq56Aa3KU33FD35yuq3I6eU5MClvdTtvgnRN0P'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True) #use this object to communicate with twitter

file_name = 'recent_id.txt'

conn = sqlite3.connect('drawingIdeas.db')
c = conn.cursor()

def art_ideas(): #replace with google cloud potentially?
    # ideas = ['pencil', 'book', 'pillow', 'towel']
    c.execute("SELECT * FROM drawingIdeas WHERE tag='Thing' OR tag='Food' ORDER BY RANDOM() LIMIT 1")
    data = c.fetchall()
    for row in data:
        idea = row[0]
    return idea

def inspo_ideas(folder): #to retrieve images stored in folder (for testing- there are 3 images in folder)
    images= glob.glob(folder + '*')
    image_open = images[randint(0,len(images))-1]
    return image_open    
    
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
            # formatting the tweet 
            theIdea = art_ideas()
            first = theIdea[0]
            # vowel formatting
            if first=="a" or first=="e" or first=="i" or first=="o" or first=="u":
                text = " Here, you can draw an "
            else:
                text = " Here, you can draw a "
            # s formatting
            if theIdea[-1]=="s":
                text = " Here, you can draw "
            api.update_status('@' + mention.user.screen_name + text + theIdea , mention.id)

def reply_image():
    print('checking')
    recent_id = retrieve_recent_id(file_name)
    mentions = api.mentions_timeline(recent_id, tweetmode='extended')

    for mention in reversed(mentions):
        print(str(mention.id) + '---' + mention.text)
        recent_id = mention.id
        store_recent_id(recent_id, file_name)
        if '#inspiration?' in mention.text.lower():
            print('found you')
            api.update_status('@' + mention.user.screen_name + 'Here you go, ', mention.id)
            api.update_with_media(inspo_pics(bot\folder), mention.id) #change source of folder 
            
while True:
    reply()
    reply_image()
    time.sleep(2) #10 sec delay

c.close()
conn.close()
