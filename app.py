from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

API_KEY = "AIzaSyDM_oCVALjVQwL3CbrqHOxShApK5tTKg6c"
MODEL = "gemini-2.0-flash"
ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json
        text = data.get("text", "")
        if not text:
            return jsonify({"error": "Empty text"}), 400

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"Analyze this resume:\n\n{text}"}
                    ]
                }
            ]
        }

        response = requests.post(ENDPOINT, json=payload, headers={"Content-Type": "application/json"})
        result = response.json()

        if "candidates" in result:
            return jsonify({"analysis": result["candidates"][0]["content"]["parts"][0]["text"]})
        else:
            return jsonify({"error": "No analysis result returned from Gemini"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
