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
@api.route("/api/leaderboard", methods=["GET"])
def leaderboard():

    try:
        conn = get_connection()

        with conn.cursor() as cur:

            cur.execute("""
                SELECT
                    telegram_id,
                    username,
                    first_name,
                    balance
                FROM users
                ORDER BY balance DESC
                LIMIT 100
            """)

            users = cur.fetchall()

        conn.close()

        return jsonify({
            "success": True,
            "leaderboard": users
        })

    except Exception as e:

        print("Leaderboard error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to load leaderboard"
        }), 500

        
@api.route("/api/auth", methods=["POST"])
def auth():
    data = request.get_json()

    telegram_id = data.get("telegram_id")
    username = data.get("username")
    first_name = data.get("first_name")
    referrer_id = data.get("referrer_id")
    
    print("Telegram ID:", telegram_id)
    print("Referral ID:", referrer_id)

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
@api.route("/api/admin/stats", methods=["GET"])
def admin_stats():

    try:
        conn = get_connection()
        cur = conn.cursor()

        # Total users
        cur.execute("SELECT COUNT(*) AS total_users FROM users;")
        total_users = cur.fetchone()["total_users"]

        # Total balance
        cur.execute("SELECT COALESCE(SUM(balance), 0) AS total_balance FROM users;")
        total_balance = cur.fetchone()["total_balance"]

        # Today's new users
        cur.execute("""
            SELECT COUNT(*) AS today_users
            FROM users
            WHERE DATE(created_at) = CURRENT_DATE;
        """)
        today_users = cur.fetchone()["today_users"]

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "total_users": total_users,
            "total_balance": total_balance,
            "today_users": today_users
        })

    except Exception as e:
        print("Admin Stats Error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to load admin stats"
        }), 500
@api.route("/api/admin/settings", methods=["POST"])
def update_admin_settings():

    data = request.get_json()

    key = data.get("setting_key")
    value = data.get("setting_value")

    if not key:
        return jsonify({
            "success": False,
            "message": "setting_key is required"
        }), 400

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE settings
            SET setting_value = %s
            WHERE setting_key = %s;
        """, (str(value), key))

        conn.commit()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "message": "Setting updated successfully"
        })

    except Exception as e:

        print("Update Settings Error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to update setting"
        }), 500

@api.route("/api/admin/users", methods=["GET"])
def admin_users():

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT
                telegram_id,
                username,
                first_name,
                balance,
                energy,
                created_at
            FROM users
            ORDER BY balance DESC;
        """)

        users = cur.fetchall()

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "users": users
        })

    except Exception as e:

        print("Admin Users Error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to load users"
        }), 500
        
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
@api.route("/api/admin/settings", methods=["GET"])
def admin_settings():

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT setting_key, setting_value
            FROM settings
            ORDER BY setting_key;
        """)

        rows = cur.fetchall()

        settings = {}

        for row in rows:
            settings[row["setting_key"]] = row["setting_value"]

        cur.close()
        conn.close()

        return jsonify({
            "success": True,
            "settings": settings
        })

    except Exception as e:

        print("Admin Settings Error:", e)

        return jsonify({
            "success": False,
            "message": "Failed to load settings"
        }), 500

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
