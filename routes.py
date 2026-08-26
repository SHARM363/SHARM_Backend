from flask import Blueprint, request, jsonify
from database import create_user

api = Blueprint("api", __name__)

@api.route("/", methods=["GET"])
def home():
    return jsonify({
        "success": True,
        "message": "Welcome to SHARM Backend API"
    })


@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "success": True,
        "status": "online"
    })


@api.route("/api/auth", methods=["POST"])
def auth():
    data = request.get_json()

    telegram_id = data.get("telegram_id")
    username = data.get("username")
    first_name = data.get("first_name")

    if not telegram_id:
        return jsonify({
            "success": False,
            "message": "telegram_id is required"
        }), 400

    create_user(telegram_id, username, first_name)

    return jsonify({
        "success": True,
        "message": "User registered successfully"
    })


@api.route("/api/tap", methods=["POST"])
def tap():
    return jsonify({
        "success": True,
        "reward": 1
    })


@api.route("/api/daily/claim", methods=["POST"])
def daily_reward():
    return jsonify({
        "success": True,
        "reward": 100,
        "day": 1
    })
