from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from models import db, User, ClickstreamLog, QuizResult
from datetime import datetime
import os
import sys

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.join(BASE_DIR, "../frontend/dist")

# Flask app setup
app = Flask(
    __name__,
    static_folder=os.path.join(FRONTEND_DIST, "static"),
    template_folder=FRONTEND_DIST
)
CORS(app)
bcrypt = Bcrypt(app)

# ---------------------------------
# Database Config
# ---------------------------------
db_url = os.environ.get("DATABASE_URL")

# Fix for Heroku/Render Postgres URL
if db_url and db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if not db_url:
    print("❌ ERROR: DATABASE_URL is not set!", file=sys.stderr)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------------------------
# Serve Vue Frontend
# ---------------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(FRONTEND_DIST, path)):
        return send_from_directory(FRONTEND_DIST, path)
    else:
        return send_from_directory(FRONTEND_DIST, "index.html")

# ---------------------------------
# Signup API
# ---------------------------------
@app.route('/api/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        name = data.get('name')
        username = data.get('username')
        password = data.get('password')

        if not name or not username or not password:
            return jsonify({"error": "Name, username, and password are required"}), 400

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(name=name, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201

    except Exception as e:
        print(f"❌ Signup error: {e}", file=sys.stderr)
        return jsonify({"error": "Internal Server Error"}), 500

# ---------------------------------
# Login API
# ---------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400

        user = User.query.filter_by(username=username).first()
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"error": "Invalid password"}), 401

        return jsonify({
            "message": "Login successful",
            "user_id": user.id,
            "username": user.username
        }), 200

    except Exception as e:
        print(f"❌ Login error: {e}", file=sys.stderr)
        return jsonify({"error": "Internal Server Error"}), 500

# ---------------------------------
# Clickstream Logging
# ---------------------------------
@app.route('/api/log', methods=['POST'])
def log_event():
    try:
        data = request.json
        new_log = ClickstreamLog(
            timestamp=datetime.now(),
            session_id=data.get('session_id'),
            user_id=data.get('user_id'),
            event_context=data.get('event_context'),
            component=data.get('component'),
            event_name=data.get('event_name'),
            description=data.get('description'),
            origin=data.get('origin'),
            ip_address=request.remote_addr
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Log recorded"}), 201
    except Exception as e:
        print(f"❌ Log error: {e}", file=sys.stderr)
        return jsonify({"error": "Internal Server Error"}), 500

# ---------------------------------
# Quiz Submission
# ---------------------------------
@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    try:
        data = request.json
        user_id = data.get('user_id')
        session_id = data.get('session_id')
        score = data.get('score')

        if not all([user_id, session_id, score is not None]):
            return jsonify({"error": "Missing required fields"}), 400

        new_result = QuizResult(user_id=user_id, session_id=session_id, score=score)
        db.session.add(new_result)
        db.session.commit()

        return jsonify({"message": "Quiz result saved successfully"}), 201
    except Exception as e:
        print(f"❌ Quiz submit error: {e}", file=sys.stderr)
        return jsonify({"error": "Internal Server Error"}), 500

# ---------------------------------
# Run Flask (Dev Mode)
# ---------------------------------
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
