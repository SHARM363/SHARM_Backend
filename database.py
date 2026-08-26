import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

def get_connection():
    return psycopg2.connect(
        Config.DATABASE_URL,
        cursor_factory=RealDictCursor
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            telegram_id BIGINT PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            balance BIGINT DEFAULT 0,
            energy INTEGER DEFAULT 1500,
            max_energy INTEGER DEFAULT 1500,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS referrals (
            id SERIAL PRIMARY KEY,
            referrer_id BIGINT NOT NULL,
            referred_id BIGINT UNIQUE NOT NULL,
            reward BIGINT DEFAULT 100,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()

def create_user(telegram_id, username, first_name):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO users (telegram_id, username, first_name)
        VALUES (%s, %s, %s)
        ON CONFLICT (telegram_id) DO NOTHING;
    """, (telegram_id, username, first_name))

    conn.commit()
    cur.close()
    conn.close()
def add_referral(referrer_id, referred_id, reward=1500):
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO referrals (referrer_id, referred_id, reward)
            VALUES (%s, %s, %s)
            ON CONFLICT (referred_id) DO NOTHING
            RETURNING id;
        """, (referrer_id, referred_id, reward))

        result = cur.fetchone()

        if result:
            cur.execute("""
                UPDATE users
                SET balance = balance + %s
                WHERE telegram_id = %s
            """, (reward, referrer_id))

        conn.commit()

        return bool(result)

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()

def get_user(telegram_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE telegram_id=%s",
        (telegram_id,)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user


def update_balance(telegram_id, amount):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET balance = balance + %s
        WHERE telegram_id = %s
        RETURNING balance;
    """, (amount, telegram_id))

    result = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if result:
        return result["balance"]

    return 0
