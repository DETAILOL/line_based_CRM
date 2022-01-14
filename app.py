#!/usr/bin/env python
# coding: utf-8

# In[1]:


# from __future__ import unicode_literals
# import os
# from flask import Flask, request, abort
# from linebot import LineBotApi, WebhookHandler
# from linebot.exceptions import InvalidSignatureError
# from linebot.models import MessageEvent, TextMessage, TextSendMessage
# import configparser
# import random


# In[2]:


# app = Flask(__name__)

# # LINE 聊天機器人的基本資料
# config = configparser.ConfigParser()
# config.read('config.txt')

# line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
# handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


# In[3]:


# # 接收 LINE 的資訊
# @app.route("/callback", methods=['POST'])
# def callback():
#     signature = request.headers['X-Line-Signature']

#     body = request.get_data(as_text=True)
#     app.logger.info("Request body: " + body)

#     try:
#         print(body, signature)
#         handler.handle(body, signature)

#     except InvalidSignatureError:
#         abort(400)

#     return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def prettyEcho(event):

#     sendString = ""
#     if "擲筊" in event.message.text:
#         sendString = divinationBlocks()
#     elif "抽簽" in event.message.text or "抽" in event.message.text:
#         sendString = drawStraws()
#     else:
#         sendString = event.message.text 

#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=sendString)
#     )
# def divinationBlocks():
#     divinationBlocksList = ["笑杯", "正杯", "正杯", "笑杯"] 
#     return divinationBlocksList[random.randint(0, len(divinationBlocksList) - 1)]

# def drawStraws():
#     drawStrawsList = ["大吉", "中吉", "小吉", "吉", "凶", "小凶", "中凶", "大凶"]
#     return drawStrawsList[random.randint(0, len(drawStrawsList) - 1)]


# In[ ]:





# In[ ]:


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

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()


# In[ ]:


# if __name__ == "__main__":
#     app.run()


# In[ ]:




