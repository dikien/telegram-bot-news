import time
import telepot
import requests
import os
from random import randint


Access_Token = os.environ['Access_Token']
bot = telepot.Bot(Access_Token)


def lambda_handler(event, context):
    event = event['body']['message']
    handle(event)


def get_news(chat_id):
    date = time.strftime("%Y-%m-%d")
    url = "https://newsdigest-yql.media.yahoo.com/v2/digest?date={0}&digest_edition=0&lang=en-AA&region=KR&region_edition=AA&timezone=9".format(date)
    headers = {'User-Agent': 'News Digest/1821 (iPhone; iOS 10.0.2; Scale/2.00)'}

    try:
        r = requests.get(url, headers=headers)

        # select rand int
        num = randint(1, 9)

        # get most favorite news
        title = r.json()['result']['items'][num]['title']
        webpageUrl = r.json()['result']['items'][num]['webpageUrl']

        # send message
        bot.sendMessage(chat_id, text=webpageUrl)

    except Exception as e:
        print(e)


def handle(msg):
    flavor = telepot.flavor(msg)

    # Check the message is normal
    if flavor == 'normal':
        content_type, chat_type, chat_id = telepot.glance2(msg)

        # Check the message is text
        if content_type == 'text':
            command = msg['text']

            if command.find('/start') != -1 or (command == '/news') != -1:
                get_news(chat_id)


bot.notifyOnMessage(lambda_handler)

