from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import redis
import os
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics


app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = "super-secret-key"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:admin123@db:5432/projectdb"

db = SQLAlchemy(app)
cache = redis.Redis(host="redis", port=6379)
metrics = PrometheusMetrics(app)

### MODELS ###

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

### AUTH ###

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User(
        username=data["username"],
        password=generate_password_hash(data["password"])
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"status": "user created"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = User.query.filter_by(username=data["username"]).first()

    if not user or not check_password_hash(user.password, data["password"]):
        return jsonify({"error": "invalid credentials"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"token": token})

def token_required(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "token missing"}), 401
        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"error": "invalid token"}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

### PROJECTS ###

@app.route("/projects", methods=["GET", "POST"])
@token_required
def projects():
    if request.method == "POST":
        p = Project(name=request.json["name"])
        db.session.add(p)
        db.session.commit()
        cache.delete("projects")
        return jsonify({"status": "created"})

    cached = cache.get("projects")
    if cached:
        return cached

    projects = Project.query.all()
    data = jsonify([{"id": p.id, "name": p.name} for p in projects])
    cache.set("projects", data.get_data())
    return data


@app.route("/process", methods=["POST"])
@token_required
def process():
    cache.rpush("tasks", "heavy_job")
    return jsonify({"status": "task sent"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
