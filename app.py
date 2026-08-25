from flask import Flask
from flask_cors import CORS
from routes import api
from database import init_db

app = Flask(__name__)
CORS(app)

app.register_blueprint(api)

# Create database tables
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
