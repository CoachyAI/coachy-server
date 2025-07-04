from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Memorie locală per utilizator
user_histories = {}
MAX_HISTORY = 5  # ultimele 5 mesaje pe utilizator

@app.route("/", methods=["GET"])
def home():
    return "Server rapid cu memorie locală funcționează!"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    user_id = data.get("user", "default")

    if not message:
        return jsonify({"error": "Mesajul este gol"}), 400

    # Istoric per user
    if user_id not in user_histories:
        user_histories[user_id] = [
            {"role": "system", "content": "Ești un antrenor prietenos care oferă sfaturi despre nutriție și fitness."}
        ]

    # Adaugă întrebarea userului
    user_histories[user_id].append({"role": "user", "content": message})
    history = user_histories[user_id][-MAX_HISTORY:]  # doar ultimele mesaje

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=history,
            max_tokens=150,
            temperature=0.7
        )
        reply = response["choices"][0]["message"]["content"]

        # Adaugă răspunsul AI în istoric
        user_histories[user_id].append({"role": "assistant", "content": reply})

        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
