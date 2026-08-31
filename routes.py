from flask import Blueprint, request, jsonify
from database import create_user, get_user, update_balance, add_referral, get_connection

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

if referrer_id and str(referrer_id) != str(telegram_id):
    add_referral(
        int(referrer_id),
        int(telegram_id)
    )

user = get_user(telegram_id)

return jsonify({
    "success": True,
    "user": user
})

@api.route("/api/me", methods=["POST"])
def me():
    data = request.get_json()

    telegram_id = data.get("telegram_id")

    if not telegram_id:
        return jsonify({
            "success": False,
            "message": "telegram_id is required"
        }), 400

    user = get_user(telegram_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    return jsonify({
        "success": True,
        "user": user
    })


@api.route("/api/tap", methods=["POST"])
def tap():
    data = request.get_json()

    telegram_id = data.get("telegram_id")
    amount = data.get("amount", 1)

    if not telegram_id:
        return jsonify({
            "success": False,
            "message": "telegram_id is required"
        }), 400

    balance = update_balance(telegram_id, amount)

    return jsonify({
        "success": True,
        "balance": balance
    })


@api.route("/api/daily/claim", methods=["POST"])
def daily_reward():
    data = request.get_json()

    telegram_id = data.get("telegram_id")

    if not telegram_id:
        return jsonify({
            "success": False,
            "message": "telegram_id is required"
        }), 400

    balance = update_balance(telegram_id, 100)

    return jsonify({
        "success": True,
        "reward": 100,
        "balance": balance
    })
@api.route("/api/referrals", methods=["POST"])
def referrals():
    data = request.get_json() or {}

    telegram_id = data.get("telegram_id")

    if not telegram_id:
        return jsonify({
            "success": False,
            "message": "telegram_id is required"
        }), 400

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT
                COUNT(*) AS total_referrals,
                COALESCE(SUM(reward), 0) AS total_reward
            FROM referrals
            WHERE referrer_id = %s
        """, (telegram_id,))

        result = cur.fetchone()

        return jsonify({
            "success": True,
            "referrals": result["total_referrals"],
            "reward": result["total_reward"]
        })

    finally:
        cur.close()
        conn.close()
