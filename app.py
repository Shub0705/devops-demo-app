from flask import Flask, request, jsonify
import json
import datetime

app = Flask(__name__)

@app.route("/")
def health():
    return "Flask webhook service is running", 200


@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    event = request.headers.get("X-GitHub-Event", "unknown")
    payload = request.json

    print("=" * 60)
    print("📌 GitHub Webhook Received")
    print("🕒 Time:", datetime.datetime.utcnow())
    print("📦 Event:", event)
    print("📄 Payload:")
    print(json.dumps(payload, indent=2))
    print("=" * 60)

    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

