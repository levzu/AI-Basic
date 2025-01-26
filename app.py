from flask import Flask, render_template, request, jsonify, send_from_directory
import os

# Импортируем наш класс бота (подправьте путь или имя, если у вас он называется иначе)
from main import GPT2XLShortAnswers  # <-- адаптируйте к вашему файлу/классу

app = Flask(__name__, template_folder='')

# Инициализация бота (загружаем модель, токенизатор и т.д.)
bot = GPT2XLShortAnswers("./local_gpt2_xl")

@app.route("/")
def index():
    # Открываем index.html (лежит в той же папке, что и app.py)
    return render_template("web.html")

# Если нужно отдавать картинки: arrow.png, avatar.png, global.png
@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory('img', filename)

# Маршрут для сообщений
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    reply = bot.generate_text(user_message)
    return jsonify({"reply": reply})

if __name__ == "__main__":
    # Запускаем Flask-сервер
    app.run(debug=True)
