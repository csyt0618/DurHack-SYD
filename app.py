from flask import Flask, render_template, request, jsonify
import json, os

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

if __name__ == '__main__':
    app.run(debug=True)
