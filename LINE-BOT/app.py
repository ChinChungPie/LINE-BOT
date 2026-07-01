import os
import json
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging.models import FlexMessage, FlexContainer

app = Flask(__name__)

# 這裡會自動讀取你在 Zeabur 後台設定的環境變數 (金鑰)
channel_access_token = os.environ.get('CHANNEL_ACCESS_TOKEN', 'YOUR_ACCESS_TOKEN')
channel_secret = os.environ.get('CHANNEL_SECRET', 'YOUR_CHANNEL_SECRET')

configuration = Configuration(access_token=channel_access_token)
handler = WebhookHandler(channel_secret)

# 這是接收 LINE 伺服器通知的專屬通道
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理接收到的文字訊息
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text

    # 判斷觀眾是否輸入特定指令
    if user_message == "SSR抽卡":
        
        # 🔻🔻🔻 請將你從 Flex Message Simulator 複製出來的 JSON 貼在下方的字典中 🔻🔻🔻
        # 注意：只需要複製 "contents" 裡面的大括號內容 (通常是以 "type": "bubble" 開頭)
        flex_json = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
  "type": "bubble",
  "body": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "text",
        "text": "🪄選取角色，玩家登入🪄",
        "color": "#FFFFFF",
        "align": "start",
        "offsetTop": "none",
        "offsetBottom": "none",
        "margin": "none"
      },
      {
        "type": "text",
        "text": "選取你的遊戲人物角色，準備登入【聲聲漫】情境劇場，蒐集你的SSR喜劇人物圖鑑，成為一級喜劇玩咖！",
        "color": "#FFFFFF",
        "wrap": true,
        "margin": "lg"
      },
      {
        "type": "text",
        "text": "　　　　　　　"
      },
      {
        "type": "text",
        "text": "請問您今天的票區是❓",
        "color": "#FFFFFF",
        "offsetTop": "none",
        "offsetBottom": "none",
        "offsetStart": "none",
        "weight": "bold",
        "wrap": false,
        "align": "center"
      },
      {
        "type": "text",
        "text": "　　　　　　"
      }
    ],
    "backgroundColor": "#3C3C3C"
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "spacing": "xxl",
    "contents": [
      {
        "type": "button",
        "style": "link",
        "height": "md",
        "action": {
          "type": "uri",
          "label": "🥇 Lv.1000",
          "uri": "https://chinchungpie.github.io/0704-SSR-Gocha-100/"
        }
      },
      {
        "type": "button",
        "style": "link",
        "height": "md",
        "action": {
          "type": "uri",
          "label": "🥈 Lv.800",
          "uri": "https://chinchungpie.github.io/0704-SSR-Gocha-50/"
        }
      },
      {
        "type": "button",
        "action": {
          "type": "uri",
          "label": "🥉 Lv.600",
          "uri": "https://chinchungpie.github.io/0704-SSR-Gocha-10/"
        },
        "height": "md",
        "style": "link"
      }
    ],
    "flex": 0,
    "margin": "none",
    "paddingAll": "xxl",
    "paddingTop": "none",
    "paddingStart": "none"
  }
}
                ]
            }
        }
        # 🔺🔺🔺 貼上 JSON 結束 🔺🔺🔺

        # 將 JSON 結構轉換成 LINE 系統看得懂的容器格式
        flex_container = FlexContainer.from_dict(flex_json)
        
        # 建立這則推播訊息 (alt_text 是觀眾在聊天室列表外觀看到的提示文字)
        flex_message = FlexMessage(alt_text="你抽取了一張 SSR 卡片！", contents=flex_container)

        # 透過 API 發送回覆給觀眾
        with ApiClient(configuration) as api_client:
            line_bot_api = MessagingApi(api_client)
            line_bot_api.reply_message_with_http_info(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[flex_message]
                )
            )

# 啟動伺服器的設定 (Zeabur 會自動分配 Port)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)