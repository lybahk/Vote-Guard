from flask import Flask, request, jsonify
import hashlib
import json
import time

app = Flask(__name__)

users = {}
votes = {}
blockchain = []

def hash_block(block):
    return hashlib.sha256(json.dumps(block, sort_keys=True).encode()).hexdigest()

def create_block(data):
    previous_hash = blockchain[-1]["hash"] if blockchain else "0"
    block = {
        "index": len(blockchain) + 1,
        "timestamp": time.time(),
        "data": data,
        "previous_hash": previous_hash
    }
    block["hash"] = hash_block(block)
    blockchain.append(block)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username, password = data["username"], hashlib.sha256(data["password"].encode()).hexdigest()
    if username in users:
        return jsonify({"message": "User already exists"}), 400
    users[username] = password
    return jsonify({"message": "Registration successful!"}), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username, password = data["username"], hashlib.sha256(data["password"].encode()).hexdigest()
    if users.get(username) == password:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/candidates", methods=["GET"])
def get_candidates():
    candidates = {
        "Mayor": ["John Doe", "Jane Smith"],
        "Governor": ["Alice Brown", "Bob Johnson"],
        "Senator": ["Emily Davis", "Michael White"]
    }
    return jsonify({"candidates": candidates}), 200

@app.route("/vote", methods=["POST"])
def vote():
    data = request.json
    username = data["username"]
    if username in votes:
        return jsonify({"message": "User has already voted!"}), 403
    votes[username] = data["votes"]
    create_block(data["votes"])
    return jsonify({"message": "Vote recorded!"}), 200

@app.route("/results", methods=["GET"])
def results():
    tally = {}
    for vote in votes.values():
        for position, candidate in vote.items():
            tally.setdefault(position, {}).setdefault(candidate, 0)
            tally[position][candidate] += 1
    return jsonify({"results": tally}), 200

if __name__ == "__main__":
    app.run(debug=True)
