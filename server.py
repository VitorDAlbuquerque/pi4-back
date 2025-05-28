from flask import Flask, jsonify
from flask_cors import CORS
from waitress import serve
from Controller.listAll.listAllBradesco import listAllBradesco
from Controller.listAll.listAllCaixa import listAllCaixa
app = Flask(__name__)
CORS(app)

@app.route("/bradesco")
def listBradesco():
    return jsonify(listAllBradesco())

@app.route("/caixa")
def listCaixa():
    return jsonify(listAllCaixa())


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=3333)
    

