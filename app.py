from flask import Flask, render_template, request, jsonify
import json
import os
from google import genai
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor


# Load API key
load_dotenv()
client = genai.Client()

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


app = Flask(__name__)



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





@app.route("/add", methods=["POST"])
def add_user():
    """Register a new user"""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"success": False, "message": "Username and password required!"})

        # Check if user already exists
        cur.execute("SELECT * FROM users WHERE username = %s;", (username,))
        existing_user = cur.fetchone()

        if existing_user:
            return jsonify({"success": False, "message": "Username already exists!"})

        # Insert new user
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s);", (username, password))
        conn.commit()

        return jsonify({"success": True, "message": "User registered successfully!"})
    
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route("/login_user", methods=["POST"])
def login_user():
    """Check login credentials"""
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"success": False, "message": "Please fill all fields"})

        # Check credentials
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s;", (username, password))
        user = cur.fetchone()

        if user:
            return jsonify({"success": True, "message": "Login successful!"})
        else:
            return jsonify({"success": False, "message": "Invalid username or password"})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


#page shown after successful login
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
