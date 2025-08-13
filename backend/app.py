from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from models import db, User, ClickstreamLog, QuizResult
from datetime import datetime
import os

# Serve Vue build
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIST = os.path.join(BASE_DIR, "../frontend/dist")

app = Flask(
    __name__,
    static_folder=os.path.join(FRONTEND_DIST, "static"),
    template_folder=FRONTEND_DIST
)
CORS(app)
bcrypt = Bcrypt(app)

# PostgreSQL config
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/webappdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------------------------
# SERVE FRONTEND
# ---------------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_vue(path):
    # Always serve index.html for Vue frontend
    return render_template("index.html")

# ---------------------------------
# SIGNUP: Create new user
# ---------------------------------
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')

    if not name or not username or not password:
        return jsonify({"error": "Name, username, and password are required"}), 400

    # Check if username exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Let PostgreSQL autoincrement assign the ID
    new_user = User(name=name, username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201

# ---------------------------------
# LOGIN: Verify user credentials
# ---------------------------------
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Find user in DB
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verify password
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid password"}), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username
    }), 200

# ---------------------------------
# CLICKSTREAM LOGGING
# ---------------------------------
@app.route('/api/log', methods=['POST'])
def log_event():
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

# ✅ New endpoint for quiz submission
@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
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

if __name__ == "__main__":
    app.run(debug=True)
