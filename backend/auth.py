from flask import Flask, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = "supersecretkey"
CORS(app)

users = {}  # Stores users in memory for now (use a database for production)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data["email"]
    password = data["password"]

    if email in users:
        return jsonify({"success": False, "message": "Email already registered!"})

    users[email] = generate_password_hash(password)
    return jsonify({"success": True, "message": "Signup successful! Please log in."})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data["email"]
    password = data["password"]

    if email not in users or not check_password_hash(users[email], password):
        return jsonify({"success": False, "message": "Invalid credentials!"})

    session["user"] = email
    return jsonify({"success": True, "message": "Login successful!"})

@app.route("/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"success": True, "message": "Logged out!"})

if __name__ == "__main__":
    app.run(debug=True)
