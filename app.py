from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "success": True,
        "name": "SHARM Backend",
        "version": "1.0.0",
        "status": "Online"
    })

@app.route("/health")
def health():
    return jsonify({
        "success": True,
        "message": "Backend is running successfully."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
