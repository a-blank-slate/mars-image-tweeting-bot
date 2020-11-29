import tweepy
import requests
import os
import datetime
import time
import schedule
from random import randint
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']
API_KEY = environ['API_KEY']

print ("Hello Making the connection with twitter!!")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.me()

print ("Connection Done!")


def tweet_image(url, message):
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message)
        os.remove(filename)
        print ("tweeted!! , going for sleep for 1 hour")
    else:
        print("Unable to download image, skipping tweet, going for sleep for 1 hour")


def get_random_image_from_nasa():
    now = datetime.datetime.now()
    date_in_string = "{}/{}/{} {}:{}:{}".format(now.day, now.month, now.year,
                                 now.hour, now.minute, now.second)
    print(date_in_string)
    random_number = randint(100, 999)
    url ="https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=" + `random_number` +"&api_key=" + API_KEY
    print("hitting NASA API with this URL :: " + url)
    request = requests.get(url)
    if request.status_code == 200:
        data = request.json()
        photos_array = data['photos']
        length = len(photos_array)
        if length!=0:
            image = photos_array[randint(0, length)]['img_src']
            print ("Found a unique image :: " + image)
            tweet_message = "Hi Tweeps, It is "+ date_in_string +", Here is an Image from MARS using NASA Opensource API"
            tweet_image(image, tweet_message )
    else:
        print("Unable to find image from NASA")


schedule.every().hour.do(get_random_image_from_nasa)

while True:
    schedule.run_pending()
    time.sleep(1)
