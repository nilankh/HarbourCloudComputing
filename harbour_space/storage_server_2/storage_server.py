# storage_server.py
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

CHUNK_DIR = "./chunks"
os.makedirs(CHUNK_DIR, exist_ok=True)


@app.route("/store_chunk/", methods=["POST"])
def store_chunk():
    data = request.json
    filename = data.get("file")
    index = data.get("index")
    chunk_data = data.get("data")

    filepath = os.path.join(CHUNK_DIR, f"{filename}_{index}.chunk")
    with open(filepath, "w") as f:
        f.write(chunk_data)

    return jsonify({"status": "stored"})


@app.route("/get_chunk/", methods=["GET"])
def get_chunk():
    filename = request.args.get("file")
    index = request.args.get("index")
    filepath = os.path.join(CHUNK_DIR, f"{filename}_{index}.chunk")

    if not os.path.exists(filepath):
        return jsonify({"error": "Not found"}), 404

    with open(filepath, "r") as f:
        data = f.read()
    return jsonify({"data": data})


@app.route("/delete_chunk/", methods=["POST"])
def delete_chunk():
    data = request.json
    filename = data.get("file")
    index = data.get("index")
    filepath = os.path.join(CHUNK_DIR, f"{filename}_{index}.chunk")

    try:
        os.remove(filepath)
        return jsonify({"status": "deleted"})
    except FileNotFoundError:
        return jsonify({"status": "already deleted"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
