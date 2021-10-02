from flask import Flask, request, abort
import os
import TimeTreeAPI

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

app = Flask(__name__)
res = TimeTreeAPI.TimeTreeAPI(0)

#環境変数取得
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
MY_USER_ID = os.environ["MY_USER_ID"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/")
def hello_world():
    return "hello world!"

@app.route("/interval")
def interval():
    try : 
        line_bot_api.broadcast(TextSendMessage(text = res.getSchedule()))
        return "push_message"
    except :
        return "Error 500"

@app.route("/update")
def update():
    try : 
        line_bot_api.push_message(MY_USER_ID, TextSendMessage(text = res.updateSchedule()))
        return "send_update_message"
    except :
        return "Error 500"
    
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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == "予定確認" :
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text = res.getSchedule())
        )
    elif event.message.text == "更新確認" :
        try :
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text = res.updateSchedule())
            )
        except : print("emptyError")


if __name__ == "__main__":
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)