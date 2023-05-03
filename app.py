# coding: utf-8

from __future__ import unicode_literals
import os
import urllib
import re
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import configparser
import random
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)
config = configparser.ConfigParser()
config.read('config.txt')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    print('---------------------')
    print(body)
    print('---------------------')
    

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 鸚鵡
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text + profile.display_name + profile.picture_url))
    
@handler.add(MessageEvent, message=TextMessage)
def ice_creamer(event):
    
    if "抽" in event.message.text:

        q_string = {'tbm': 'isch', 'q': event.message.text.replace('抽','')}
        url = f"https://www.google.com/search?{urllib.parse.urlencode(q_string)}/"
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'}

        req = urllib.request.Request(url, headers = headers)
        conn = urllib.request.urlopen(req)

        print('fetch conn finish')

        pattern = 'img data-src="\S*"'
        img_list = []

        for match in re.finditer(pattern, str(conn.read())):
            img_list.append(match.group()[14:-1])

        random_img_url = img_list[random.randint(0, len(img_list)+1)]
        print('fetch img url finish')
        print(random_img_url)

        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(
                original_content_url=random_img_url,
                preview_image_url=random_img_url
            )
        )



if __name__ == "__main__":
    app.run()






