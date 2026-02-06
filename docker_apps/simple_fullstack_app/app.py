from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
POSTGRES_USER = os.environ.get("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "admin123")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "usersdb")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", "5432")

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def as_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}

# Routes
@app.route("/")
def home():
    return "User Management App - Dockerized with PostgreSQL"

@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.as_dict() for user in users])

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and email are required"}), 400
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(name=data["name"], email=data["email"])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.as_dict()), 201

if __name__ == "__main__":
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
