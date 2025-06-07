from flask import Flask, jsonify, request
from flask_cors import CORS
from waitress import serve
from Controller.listAll.listAllBradesco import listAllBradesco
from Controller.listAll.listAllCaixa import listAllCaixa
from Controller.auth.register import register
from Controller.auth.login import login
from Controller.auth.auth_utils import verify_token
from Controller.auth.delete_user import delete_user
from Controller.listAll.test_bradesco_db import upload_test_bradesco, delete_test_bradesco

app = Flask(__name__)
CORS(app)


@app.route("/register")
def register_route():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    if not username or not password or not email:
        return jsonify({"error": "Missing fields"}), 400
    if register(username, password, email):
        return jsonify({"message": "User registered successfully"})
    return jsonify({"error": "User already exists"}), 409

@app.route("/login")
def login_route():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    token = login(username, password)
    if token:
        return jsonify({"token": token})
    return jsonify({"error": "Invalid credentials"}), 401

def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Missing token'}), 401
        token = auth_header.split(" ")[-1]
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/protected")
@token_required
def protected_route():
    return jsonify({"message": "You are authenticated!"})


@app.route("/bradesco")
@token_required
def listBradesco():
    return jsonify(listAllBradesco())

@app.route("/caixa")
@token_required
def listCaixa():
    return jsonify(listAllCaixa())

@app.route("/delete_user")
@token_required
def delete_user_route():
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[-1]
    payload = verify_token(token)
    username = payload.get("username") if payload else None
    if not username:
        return jsonify({"error": "Invalid token"}), 401
    if delete_user(username):
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"error": "User not found"}), 404

@app.route("/test/upload_bradesco")
def upload_bradesco_route():
    upload_test_bradesco()
    return jsonify({"message": "Test Bradesco data uploaded."})

@app.route("/test/delete_bradesco")
def delete_bradesco_route():
    delete_test_bradesco()
    return jsonify({"message": "Test Bradesco data deleted."})


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=3333)


