from flask import Flask, jsonify
from flask_cors import CORS
from waitress import serve
from Controller.bradescoInit import bradescoInit
from Controller.bradescoFull import bradescoFull
app = Flask(__name__)
CORS(app)

@app.route("/list")
def list():
    return jsonify(bradescoFull())

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=3333)