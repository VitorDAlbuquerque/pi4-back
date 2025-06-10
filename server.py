from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from waitress import serve
from Controller.listAll.listAllItau import listAllItau
from Controller.listAll.listAllBradesco import listAllBradesco
from Controller.listAll.listAllCaixa import listAllCaixa
from Controller.listAll.listAllSantander import listAllSantander
from Controller.auth.register import register
from Controller.auth.login import login
from Controller.auth.auth_utils import verify_token
from Controller.auth.delete_user import delete_user
from Controller.listAll.test_bradesco_db import upload_all_banks, delete_all_banks
from Controller.folder.crudFolder import (
    create_folder, list_folders, read_folder, update_folder, delete_folder,
    add_property_to_folder, remove_property_from_folder
)
from Controller.filter.filter import filter_bradesco
from Controller.listAll.listPropertys import list_all_propertys

app = Flask(__name__)
CORS(app)


@app.route("/register", methods=["POST"])
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

@app.route("/login", methods=["POST"])
def login_route():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    token = login(username, password)
    if token:
        return jsonify({"token": token, "username": username, "password": password})
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

@app.route("/userInfo", methods=["GET", "OPTIONS"])
@cross_origin()
@token_required
def user_info_route():
    if request.method == "OPTIONS":
        return '', 200
    auth_header = request.headers.get('Authorization')
    token = auth_header.split(" ")[-1]
    payload = verify_token(token)
    if not payload:
        return jsonify({"error": "Invalid token"}), 401
    username = payload.get("username")
    return jsonify({
        "username": username,
        "password": payload.get("password"),
        "email": payload.get("email"),
        "message": "User authenticated successfully"
    })
@app.route("/protected", methods=["GET"])
@token_required
def protected_route():
    return jsonify({"message": "You are authenticated!"})


@app.route("/bradesco", methods=["GET"])

def listBradesco():
    return jsonify(listAllBradesco())

@app.route("/itau", methods=["GET"])

def listItau():
    return jsonify(listAllItau())

@app.route("/santander", methods=["GET"])

def listSantander():
    return jsonify(listAllSantander())


@app.route("/caixa", methods=["GET"])

def listCaixa():
    return jsonify(listAllCaixa())

@app.route("/delete_user", methods=["DELETE"])
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
    upload_all_banks()
    return jsonify({"message": "Test Bradesco data uploaded."})

@app.route("/test/delete_bradesco")
def delete_bradesco_route():
    delete_all_banks()
    return jsonify({"message": "Test Bradesco data deleted."})

@app.route("/create_folder", methods=["POST"])
@token_required
def create_folder_route():
    data = request.json
    name = data.get("name")
    if not name:
        return jsonify({"error": "Missing folder name"}), 400
    result = create_folder(name)
    return jsonify(result)

@app.route("/list_folders", methods=["GET"])
@token_required
def list_folders_route():
    result = list_folders()
    return jsonify(result)

@app.route("/read_folder", methods=["GET"])
@token_required
def read_folder_route():
    data = request.json
    folder_id = data.get("folder_id")
    if not folder_id:
        return jsonify({"error": "Missing folder_id"}), 400
    result = read_folder(folder_id)
    if result:
        return jsonify(result)
    return jsonify({"error": "Folder not found"}), 404

@app.route("/update_folder", methods=["PUT"])
@token_required
def update_folder_route():
    data = request.json
    folder_id = data.get("folder_id")
    name = data.get("name")
    if not folder_id or not name:
        return jsonify({"error": "Missing folder_id or name"}), 400
    result = update_folder(folder_id, name)
    if result:
        return jsonify(result)
    return jsonify({"error": "Folder not found"}), 404

@app.route("/delete_folder", methods=["DELETE"])
@token_required
def delete_folder_route():
    data = request.json
    folder_id = data.get("folder_id")
    if not folder_id:
        return jsonify({"error": "Missing folder_id"}), 400
    result = delete_folder(folder_id)
    if result:
        return jsonify({"message": "Folder deleted successfully"})
    return jsonify({"error": "Folder not found"}), 404

@app.route("/add_property_to_folder", methods=["POST"])
@token_required
def add_property_to_folder_route():
    data = request.json
    folder_id = data.get("folder_id")
    property_data = data.get("property")
    if not folder_id or property_data is None:
        return jsonify({"error": "Missing folder_id or property"}), 400
    result = add_property_to_folder(folder_id, property_data)
    if result:
        return jsonify(result)
    return jsonify({"error": "Folder not found"}), 404

@app.route("/remove_property_from_folder", methods=["DELETE"])
@token_required
def remove_property_from_folder_route():
    data = request.json
    folder_id = data.get("folder_id")
    property_id = data.get("property_id")
    if not folder_id or not property_id:
        return jsonify({"error": "Missing folder_id or property_id"}), 400
    result = remove_property_from_folder(folder_id, property_id)
    if result:
        return jsonify(result)
    return jsonify({"error": "Folder or property not found"}), 404

@app.route("/listPropertys", methods=["GET"])
def list_propertys_route():
    results = list_all_propertys()
    return jsonify(results)

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



print("Starting server on port 3333")
serve(app, host="0.0.0.0", port=3333)