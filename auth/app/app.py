from flask import Flask, request, jsonify
import jwt, datetime, os

app = Flask(__name__)

# Read secret from environment variable
SECRET_KEY = os.environ.get("JWT_SECRET", "dev-secret")  # fallback for local/minikube

users = {}

# ------------------------
# Basic routes
# ------------------------

@app.route("/")
def home():
    return jsonify({"status": "Auth service is running"})

@app.route("/health")
def health():
    return jsonify({"status": "OK"})

# ------------------------
# Auth routes
# ------------------------

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400

    if data["username"] in users:
        return jsonify({"error": "User already exists"}), 400

    users[data["username"]] = data["password"]
    return jsonify({"message": "User registered successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400

    if users.get(data["username"]) != data["password"]:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "user": data["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return jsonify({"token": token})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

