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
from Controller.folder.crudFolder import (
    create_folder, read_folder, update_folder, delete_folder,
    add_property_to_folder, remove_property_from_folder
)
from Controller.filter.filter import filter_bradesco

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

@app.route("/folder", methods=["POST"])
@token_required
def create_folder_route():
    data = request.json
    folder_name = data.get("name")
    if not folder_name:
        return jsonify({"error": "Missing folder name"}), 400
    folder_id = create_folder(folder_name)
    if folder_id:
        return jsonify({"message": "Folder created", "id": folder_id})
    return jsonify({"error": "Folder name already exists"}), 409

@app.route("/folder/<folder_id>", methods=["GET"])
@token_required
def read_folder_route(folder_id):
    folder = read_folder(folder_id)
    if folder:
        return jsonify(folder)
    return jsonify({"error": "Folder not found"}), 404

@app.route("/folder/<folder_id>", methods=["PUT"])
@token_required
def update_folder_route(folder_id):
    data = request.json
    new_name = data.get("name")
    if not new_name:
        return jsonify({"error": "Missing new folder name"}), 400
    if update_folder(folder_id, new_name):
        return jsonify({"message": "Folder updated"})
    return jsonify({"error": "Folder not found"}), 404

@app.route("/folder/<folder_id>", methods=["DELETE"])
@token_required
def delete_folder_route(folder_id):
    if delete_folder(folder_id):
        return jsonify({"message": "Folder deleted"})
    return jsonify({"error": "Folder not found"}), 404

@app.route("/folder/<folder_id>/add_property", methods=["POST"])
@token_required
def add_property_route(folder_id):
    data = request.json
    property_id = data.get("property_id")
    if not property_id:
        return jsonify({"error": "Missing property_id"}), 400
    if add_property_to_folder(folder_id, property_id):
        return jsonify({"message": "Property added to folder"})
    return jsonify({"error": "Folder or property not found"}), 404

@app.route("/folder/<folder_id>/remove_property", methods=["POST"])
@token_required
def remove_property_route(folder_id):
    data = request.json
    property_id = data.get("property_id")
    if not property_id:
        return jsonify({"error": "Missing property_id"}), 400
    if remove_property_from_folder(folder_id, property_id):
        return jsonify({"message": "Property removed from folder"})
    return jsonify({"error": "Folder or property not found"}), 404

@app.route("/filter_bradesco", methods=["POST"])
@token_required
def filter_bradesco_route():
    data = request.json
    value = data.get("value")
    state = data.get("state")
    city = data.get("city")
    area = data.get("area")
    date = data.get("date")
    results = filter_bradesco(
        value=value,
        state=state,
        city=city,
        area=area,
        date=date
    )
    return jsonify(results)


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=3333)


