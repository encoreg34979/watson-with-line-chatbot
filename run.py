# encoding: utf-8
import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import * #把linebot models 全部拉進來
from watson_developer_cloud import AssistantV1
import json
from pprint import pprint


class ChatBot:
    line_access_tocken = 'dZD6cK/tb0+UUwApRdoRx++pzxPiCh+7Me3fFTnduf2tGCo3vX/zUY+e5cxz9miWYJhwPf2NbSonJX9wXXOy8zZKUR2QZJcK5hlbYo9C4sA+ZUQt+OQ7pW8bMqgBHBq+3L0E5Lp7PxV8s+mdZnMg5gdB04t89/1O/w1cDnyilFU='
    line_channel_secret = 'b1be23e0bd3431d2d809e346743b75ac'
    iam_apikey = 'i6qDBImCNiuXFiQb_Ho9EwBKwVmsoUD_pCl4fBlfT2Lg'
    url = 'https://gateway.watsonplatform.net/assistant/api'
    workspace_id='7eb5e40b-e90f-46c3-bcb9-1e53c0333b5f'
    #URL:https://assistant-chat-us-south.watsonplatform.net/web/public/05044ecf-dc4a-41be-915f-42ee56503b4d
    msg_receive = ''
    msg_reply = ''
    msg_image = ''
    lenthOfText = 0 #選取句子用

app = Flask(__name__)
line_bot_api = LineBotApi(ChatBot.line_access_tocken)
handler = WebhookHandler(ChatBot.line_channel_secret)

assistant = AssistantV1(
    version = '2018-09-20',
    iam_apikey = ChatBot.iam_apikey,
    url = ChatBot.url
    )

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    ChatBot.msg_receive = event.message.text
    json_reply = assistant.message(
    workspace_id = ChatBot.workspace_id, 
    input = {'text':ChatBot.msg_receive}).get_result()
    if json_reply['output']['generic'][0]['response_type'] == 'text':
        ChatBot.msg_reply = json_reply['output']['text'][0]
        line_bot_api.reply_message(event.reply_token,TextSendMessage(ChatBot.msg_reply))
    elif json_reply['output']['generic'][0]['response_type'] == 'image':
        ChatBot.msg_reply = json_reply['output']['generic'][0]['title']
        ChatBot.msg_image = json_reply['output']['generic'][0]['source']
 #       line_bot_api.reply_message(event.reply_token,TextSendMessage(ChatBot.msg_reply))
        line_bot_api.reply_message(event.reply_token,ImageSendMessage(original_content_url=ChatBot.msg_image, preview_image_url=ChatBot.msg_image))

    #print(ChatBot.msg_receive)
    #print(ChatBot.msg_reply)
    #print(json.dumps(ChatBot.msg_reply, indent=2))
    

if __name__ == "__main__":
    app.run()
    


#Receive Json code from Line
    # {"events":[{
    #     "type":"message",
    #     "replyToken":"cc79dbed39df40019ed54511be8d77f6",
    #     "source":{
    #         "userId":"Ue22ff760aa6cde4390c6d5567d5aa5f5",
    #         "type":"user"
    #         },
    #     "timestamp":1496211335206,
    #     "message":{
    #         "type":"text",
    #         "id":"6167354628626",
    #         "text":"跑"
    #         }
    #     }]
    # }

#Receive Jason code from Line
    # {   
    #     'input': {'text': 'Hello'}, 
    #     'intents': [], 
    #     'context': 
    #     {
    #         'conversation_id': '4d173d82-a606-4b07-b6aa-3d5f92be54aa', 
    #         'system': 
    #         {
    #             'dialog_turn_counter': 1, 
    #                 'dialog_request_counter': 1, 
    #                 '_node_output_map': {'其他事情': [0]}, 
    #                 'dialog_stack': [{'dialog_node': 'root'}], 
    #                 'branch_exited_reason': 'completed', 
    #                 'branch_exited': True
    #                     }
    #             }, 
    #     'entities': [], 
    #     'output': {
    #         'log_messages': [], 
    #         'nodes_visited': ['其他事情'], 
    #         'text': ['我不瞭解您的問題。您可以換種方式說明']
    #         }
    # }
