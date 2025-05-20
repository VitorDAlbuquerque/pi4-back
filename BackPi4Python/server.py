from flask import Flask, jsonify
from waitress import serve
from Controller.main import scrapper
app = Flask(__name__)

@app.route("/list")
def list():
    return jsonify(scrapper())

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=3333)