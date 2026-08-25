from flask import Blueprint, request, jsonify

api = Blueprint("api", __name__)

# Home
@api.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Welcome to SHARM Backend API"
    })


# Health Check
@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "status": "online"
    })


# Telegram Login
@api.route("/api/auth", methods=["POST"])
def auth():
    data = request.json

    return jsonify({
        "success": True,
        "message": "Authentication successful",
        "user": data
    })


# Tap
@api.route("/api/tap", methods=["POST"])
def tap():

    return jsonify({
        "success": True,
        "reward": 1,
        "message": "Tap successful"
    })


# Daily Reward
@api.route("/api/daily/claim", methods=["POST"])
def daily_reward():

    return jsonify({
        "success": True,
        "reward": 100,
        "day": 1,
        "message": "Daily reward claimed"
    })
