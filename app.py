from flask import Flask, render_template, request, jsonify
import json
import os
from google import genai
from dotenv import load_dotenv
import psycopg2

# Load API key
load_dotenv()
client = genai.Client()

app = Flask(__name__)

FILENAME = "vault.json"

def load_data():
    if os.path.exists(FILENAME):
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"user": [], "password": []}

def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    # ✅ show login by default instead of blank home
    return render_template('login.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route("/users")
def get_users():
    return jsonify(load_data())

@app.route("/add", methods=["POST"])
def add_user():
    data = load_data()
    new_user = request.json.get("username")
    new_pass = request.json.get("password")

    # ✅ Basic validation
    if not new_user or not new_pass:
        return jsonify({"success": False, "message": "Username and password required!"})

    if new_user in data["user"]:
        return jsonify({"success": False, "message": "Username already exists!"})

    data["user"].append(new_user)
    data["password"].append(new_pass)
    save_data(data)

    return jsonify({"success": True, "message": "User registered successfully!"})

# Optional: test route for JS → Flask communication
@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    name = data.get('name', 'Guest')
    return jsonify({'message': f'Hello {name}, Flask received your data!'})

# ✅ Optional: page shown after successful login
@app.route("/home")
def after_login():
    return render_template("home.html")



#GEMINI API 
@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        sliders = data.get('sliders', {})
        paragraph = data.get('paragraph', '')

        prompt = f"""
You are a friendly culinary assistant. The user gave these mood values and a short note.

MOOD DATA: {json.dumps(sliders, indent=2)}
USER NOTE: \"\"\"{paragraph.strip()}\"\"\"

Your task:
1. Suggest one dish that matches their current mood or helps them feel better.
2. Explain briefly *why* that dish suits their state.
3. List 3–8 key ingredients.
4. Add one short serving or preparation suggestion.
5. Return **only valid JSON** with:
   dish, reason, ingredients (array), suggestion, score (0–100).
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        raw = response.text

        import re
        try:
            result = json.loads(raw)
        except Exception:
            m = re.search(r'(\{[\s\S]*\})', raw)
            result = json.loads(m.group(1)) if m else {"raw": raw}

        return jsonify({"ok": True, "result": result})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
