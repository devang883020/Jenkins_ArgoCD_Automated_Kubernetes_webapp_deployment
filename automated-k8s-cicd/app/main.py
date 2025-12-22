from flask import Flask, jsonify
import socket
import datetime
import os
import platform

app = Flask(__name__)

APP_NAME = os.getenv("APP_NAME", "Python Flask DevOps WebApp by devang Kubde")
APP_VERSION = os.getenv("APP_VERSION", "1.0.5")
ENVIRONMENT = os.getenv("ENVIRONMENT", "Development")

@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>{APP_NAME}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: linear-gradient(120deg, #1e3c72, #2a5298);
                color: white;
                text-align: center;
                padding: 40px;
            }}
            .card {{
                background: rgba(0,0,0,0.3);
                padding: 30px;
                border-radius: 15px;
                width: 70%;
                margin: auto;
                box-shadow: 0px 0px 20px rgba(0,0,0,0.4);
            }}
            h1 {{
                color: #00ffcc;
            }}
            .badge {{
                display: inline-block;
                padding: 8px 16px;
                background: #00ffcc;
                color: #000;
                border-radius: 20px;
                font-weight: bold;
            }}
            footer {{
                margin-top: 30px;
                font-size: 14px;
                opacity: 0.8;
            }}
        </style>
    </head>

    <body>
        <div class="card">
            <h1>🚀 {APP_NAME}</h1>
            <p class="badge">Running in {ENVIRONMENT}</p>

            <p><b>Hostname:</b> {socket.gethostname()}</p>
            <p><b>Time:</b> {datetime.datetime.now()}</p>
            <p><b>Python Version:</b> {platform.python_version()}</p>
            <p><b>App Version:</b> {APP_VERSION}</p>

            <hr>
            <p>✅ Docker Image Built Successfully</p>
            <p>⚙️ Jenkins CI/CD Pipeline</p>
            <p>📦 Helm Charts Deployed</p>
            <p>🔄 ArgoCD GitOps Enabled</p>
        </div>

        <footer>
            Built by Devang kubde | DevOps | Kubernetes | Cloud
        </footer>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return jsonify(
        status="UP",
        app=APP_NAME,
        version=APP_VERSION,
        timestamp=str(datetime.datetime.now())
    )

@app.route("/api/info")
def info():
    return jsonify(
        app_name=APP_NAME,
        version=APP_VERSION,
        environment=ENVIRONMENT,
        hostname=socket.gethostname(),
        python_version=platform.python_version()
    )

@app.route("/metrics")
def metrics():
    return jsonify(
        uptime="Running",
        container="Docker / Kubernetes ready",
        cicd="Jenkins + ArgoCD"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
