from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"message": "Bienvenue sur mon API", "status": "ok"})


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/hello/<name>")
def hello(name):
    return jsonify({"message": f"Bonjour {name} !"})


@app.route("/add/<a>/<b>")
def add(a, b):
    try:
        first = int(a)
        second = int(b)
    except ValueError:
        return jsonify({"error": "Les parametres doivent etre des entiers"}), 400

    return jsonify({"result": first + second})


if __name__ == "__main__":
    app.run(debug=True)
