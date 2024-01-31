from flask import Flask, request, jsonify
from ultrabot import ultraChatBot
import json

app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():
    if request.method == "POST":
        try:
            bot = ultraChatBot(request.json)
            response = bot.Processingـincomingـmessages()
            return jsonify({"response": (response)})
        except Exception as e:
            return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
