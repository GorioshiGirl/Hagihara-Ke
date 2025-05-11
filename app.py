from flask import Flask, request, abort
import os
import json
import requests

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Renderが環境変数で渡すポート番号を取得
    app.run(host="0.0.0.0", port=port)        # すべての外部アクセスを受け付ける設定

app = Flask(__name__)

# 環境変数からLINEのチャンネルアクセストークンを取得
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_REPLY_ENDPOINT = "https://api.line.me/v2/bot/message/reply"

@app.route("/", methods=["GET"])
def index():
    return "LINE Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    body = request.get_data(as_text=True)
    try:
        events = json.loads(body)["events"]
        for event in events:
            if event["type"] == "message" and event["message"]["type"] == "text":
                reply_token = event["replyToken"]
                user_message = event["message"]["text"]
                reply_message = generate_reply(user_message)
                send_line_reply(reply_token, reply_message)
    except Exception as e:
        print(f"Error: {e}")
        abort(400)
    return "OK"

def generate_reply(user_text):
    if user_text == "こんにちは":
        return "こんにちは！今日はいい天気ですね ☀️"
    elif user_text == "さようなら":
        return "またね〜！👋"
    else:
        return f"「{user_text}」ですね！それについてはまだ学習中です💭"

def send_line_reply(token, message):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LINE_CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": token,
        "messages": [{"type": "text", "text": message}]
    }
    requests.post(LINE_REPLY_ENDPOINT, headers=headers, json=payload)
