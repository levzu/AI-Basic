from flask import Flask, render_template, request, jsonify, send_from_directory
import os

from main import GPT2XLShortAnswers

app = Flask(__name__, template_folder='')

bot = GPT2XLShortAnswers("./local_gpt2_xl")

@app.route("/")
def index():
    return render_template("web.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory('img', filename)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = bot.generate_text(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)
