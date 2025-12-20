from flask import Flask, jsonify
import socket
import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return f"""
    <h1>🚀 Python Flask Web App with Jenkins CICD pipeline!!</h1>
    <p><b>Hostname:</b> {socket.gethostname()}</p>
    <p><b>Time:</b> {datetime.datetime.now()}</p>
    <p>Status: Running successfully</p>
    """

@app.route("/health")
def health():
    return jsonify(
        status="UP",
        service="python-webapp",
        time=str(datetime.datetime.now())
    )

@app.route("/api/info")
def info():
    return jsonify(
        app="Flask Docker Web App",
        version="1.0",
        author="Devang"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
