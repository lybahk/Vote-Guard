from flask import Flask, request, jsonify, session
import hashlib
import json
from time import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Blockchain Structure
class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_votes = []
        self.voted_users = set()  # Tracks users who have voted
        self.create_block(previous_hash="1")

    def create_block(self, previous_hash):
        block = {
            "index": len(self.chain) + 1,
            "timestamp": time(),
            "votes": self.current_votes,
            "previous_hash": previous_hash,
            "hash": self.hash_block(self.current_votes, previous_hash)
        }
        self.current_votes = []
        self.chain.append(block)
        return block

    def add_vote(self, user, votes):
        if user in self.voted_users:
            return False  # Prevent duplicate voting

        self.current_votes.append({"user": user, "votes": votes})
        self.voted_users.add(user)
        return True

    def get_last_block(self):
        return self.chain[-1]

    def hash_block(self, votes, previous_hash):
        block_string = json.dumps(votes, sort_keys=True) + previous_hash
        return hashlib.sha256(block_string.encode()).hexdigest()

blockchain = Blockchain()

@app.route("/submit_vote", methods=["POST"])
def submit_vote():
    if "user" not in session:
        return jsonify({"success": False, "message": "Please log in to vote."})

    user = session["user"]
    votes = request.json

    if blockchain.add_vote(user, votes):
        blockchain.create_block(previous_hash=blockchain.get_last_block()["hash"])
        return jsonify({"success": True, "message": "Vote successfully submitted!"})
    else:
        return jsonify({"success": False, "message": "You have already voted!"})

@app.route("/get_results", methods=["GET"])
def get_results():
    results = {}
    for block in blockchain.chain:
        for vote in block["votes"]:
            for position, candidate in vote["votes"].items():
                if position not in results:
                    results[position] = {}
                if candidate in results[position]:
                    results[position][candidate] += 1
                else:
                    results[position][candidate] = 1
    return jsonify(results)

if __name__ == "__main__":
    app.secret_key = "supersecretkey"
    app.run(debug=True)
