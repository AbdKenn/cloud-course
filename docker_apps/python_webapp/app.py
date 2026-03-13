from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({
        "message": "Hello from Flask in Docker",
        "container_id": socket.gethostname(),
        "time": datetime.datetime.utcnow().isoformat()
    })

@app.route("/course")
def course():
    return "Cloud & Docker course // containerized app running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
