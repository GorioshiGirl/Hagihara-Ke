from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    # LINEからのWebhookイベントを受け取ったときの処理
    print(request.json)  # 受け取ったデータを表示
    return "OK", 200  # ステータスコード200を返す

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
