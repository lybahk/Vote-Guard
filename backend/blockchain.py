from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

VOTES_FILE = "votes.json"

# Function to load votes from JSON
def load_votes():
    if os.path.exists(VOTES_FILE):
        with open(VOTES_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save votes
def save_votes(votes):
    with open(VOTES_FILE, "w") as file:
        json.dump(votes, file, indent=4)

# API Endpoint to Submit a Vote
@app.route('/submit_vote', methods=['POST'])
def submit_vote():
    data = request.json
    position = data.get("position")
    candidate = data.get("candidate")

    if not position or not candidate:
        return jsonify({"error": "Invalid vote data"}), 400

    votes = load_votes()
    if position not in votes:
        votes[position] = {}

    if candidate in votes[position]:
        votes[position][candidate] += 1
    else:
        votes[position][candidate] = 1

    save_votes(votes)
    return jsonify({"message": "Vote submitted successfully!", "votes": votes})

# API Endpoint to Fetch Results
@app.route('/get_results', methods=['GET'])
def get_results():
    votes = load_votes()
    return jsonify(votes)

if __name__ == '__main__':
    app.run(port=5000)
