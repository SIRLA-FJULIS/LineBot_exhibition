import os
from flask import Flask, request, abort
from csrf_scraw import get_datas
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, 
    TemplateSendMessage, CarouselTemplate, CarouselColumn,
    URITemplateAction
)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))


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
    print(event.message.text)
    if event.message.text == '最新展覽':
        datas = get_datas()
        columns= []
        for i, d in enumerate(datas):
            print(d['title'])
            column = CarouselColumn(
                thumbnail_image_url = d['img'],
                title = d['title'],
                text = d['text'],
                actions = [
                    URITemplateAction(
                        label = '展覽介紹連結',
                        uri = d['url']
                    )
                ]
            )
            columns.append(column)

        carousel_template_message = TemplateSendMessage(
            alt_text = "展覽輪播",
            template = CarouselTemplate(
                columns = columns
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            carousel_template_message
        )
        
if __name__ == "__main__":
    app.run()