from flask import Flask, request, abort
import os
import TimeTreeAPI
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)
res = TimeTreeAPI.TimeTreeAPI(0)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/interval")
def interval():
    try : 
        return "OK"
        # line_bot_api.broadcast(TextSendMessage(text = res.getSchedule()))
    except : return "Error 500"
    
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # userId を取得 (1)
    body_json = json.loads(body)
    app.logger.info("User Id: {}".format(body_json["events"][0]["source"]["userId"]))
    print(body_json["events"][0]["source"]["userId"])

    text_message = body_json["events"][0]["source"]["userId"]
    try:
        line_bot_api.push_message(SEND_USER_ID, TextSendMessage(text=text_message))
    except LineBotApiError as e:
        print(e)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "予定確認" :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = event.source.userId)
            # TextSendMessage(text = res.getSchedule())
        )


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)