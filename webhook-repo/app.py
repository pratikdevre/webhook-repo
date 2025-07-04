# Import necessary libraries
from flask import Flask, request, jsonify  # For Flask web server and API handling
from flask_cors import CORS  # To allow cross-origin requests from the frontend
from pymongo import MongoClient  # MongoDB client
from config import MONGO_URI  # MongoDB connection string from config file
from datetime import datetime  # For timestamping

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS so frontend (JS) can call backend

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client['webhook_db']  # Database name
collection = db['github_events']  # Collection name

# Route to handle incoming GitHub Webhooks
@app.route("/webhook", methods=["POST"])
def github_webhook():
    data = request.json  # Get JSON payload from webhook POST

    # Determine the type of GitHub action
    action_type = None
    if "pusher" in data:
        action_type = "PUSH"
    elif "pull_request" in data:
        if data["action"] == "opened":
            action_type = "PULL_REQUEST"
        elif data["action"] == "closed" and data["pull_request"]["merged"]:
            action_type = "MERGE"

    # Build a payload to insert into MongoDB
    payload = {
        "request_id": data.get("after") or data.get("pull_request", {}).get("id"),
        "author": data.get("pusher", {}).get("name") or data.get("sender", {}).get("login"),
        "action": action_type,
        "from_branch": data.get("pull_request", {}).get("head", {}).get("ref") if "pull_request" in data else None,
        "to_branch": data.get("pull_request", {}).get("base", {}).get("ref") if "pull_request" in data else data.get("ref", "").split("/")[-1],
        "timestamp": datetime.utcnow().isoformat()
    }

    # Insert the event into MongoDB
    collection.insert_one(payload)

    # Return response to GitHub
    return jsonify({"message": "Webhook received!"}), 200

# Route to return stored GitHub events to frontend
@app.route("/events", methods=["GET"])
def get_events():
    # Fetch events from MongoDB, sorted by newest first, excluding internal _id
    events = list(collection.find({}, {"_id": 0}).sort("timestamp", -1))
    return jsonify(events)

# Start Flask app
if __name__ == "__main__":
    app.run(debug=True)
