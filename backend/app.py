from flask import Flask, request, jsonify, session
import sqlite3
import hashlib
import json
import time
from blockchain import Blockchain

app = Flask(__name__)
app.secret_key = "supersecurekey"  # Session key for remembering login

# Initialize SQLite Database
conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, 
    email TEXT UNIQUE, 
    password TEXT
)
""")
conn.commit()

# Initialize Blockchain
blockchain = Blockchain()

# ---- API ROUTES ----

# Register User
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    hashed_password = hashlib.sha256(data["password"].encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", 
                       (data["name"], data["email"], hashed_password))
        conn.commit()
        return jsonify({"success": True, "message": "User registered successfully!"})
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email already exists!"})

# Login User
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    hashed_password = hashlib.sha256(data["password"].encode()).hexdigest()
    cursor.execute("SELECT * FROM users WHERE email = ? AND password = ?", 
                   (data["email"], hashed_password))
    user = cursor.fetchone()
    if user:
        session["user"] = user[1]
        return jsonify({"success": True, "message": "Login successful!", "user": user[1]})
    else:
        return jsonify({"success": False, "message": "Invalid credentials!"})

# Vote Submission
@app.route("/vote", methods=["POST"])
def vote():
    if "user" not in session:
        return jsonify({"success": False, "message": "User not logged in!"})

    data = request.json
    vote_data = {"user": session["user"], "votes": data["votes"]}
    
    block = blockchain.create_block(vote=vote_data)
    
    return jsonify({"success": True, "message": "Vote recorded!", "block": block})

# Get Results
@app.route("/get_results", methods=["GET"])
def get_results():
    return jsonify({"chain": blockchain.chain, "length": len(blockchain.chain)})

if __name__ == "__main__":
    app.run(debug=True)
