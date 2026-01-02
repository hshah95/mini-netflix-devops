from flask import Flask, request, jsonify
import jwt, datetime, os

app = Flask(__name__)

# Read secret from environment variable
SECRET_KEY = os.environ.get("JWT_SECRET")

if not SECRET_KEY:
    raise Exception("JWT_SECRET is not set")

users = {}

@app.route("/register", methods=["POST"])
def register():
    data = request.json

    if data["username"] in users:
        return jsonify({"error": "User already exists"}), 400

    users[data["username"]] = data["password"]
    return jsonify({"message": "User registered successfully"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json

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
    app.run(host="0.0.0.0", port=5001)
