import os
from flask import Flask, request, jsonify, send_from_directory

from sentinelcat_detection_rules import classify

APP_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

@app.route("/installation", methods=["GET"])
@app.route("/installation.html", methods=["GET"])
def installation():
    return send_from_directory(APP_DIR, "installation.html")

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(APP_DIR, "index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "service": "SentinelCAT"}), 200


@app.route("/api/classify", methods=["POST"])
def api_classify():
    payload = None

    if request.is_json:
        payload = request.get_json(silent=True)
    else:
        raw = request.form.get("payload")
        if raw:
            try:
                import json
                payload = json.loads(raw)
            except Exception:
                return jsonify({
                    "ok": False,
                    "error": "Invalid JSON in form field 'payload'."
                }), 400

    if payload is None:
        return jsonify({
            "ok": False,
            "error": "No JSON payload provided. Send JSON body or form field 'payload'."
        }), 400

    try:
        result = classify(payload)
        return jsonify({"ok": True, "result": result}), 200
    except Exception as e:
        return jsonify({
            "ok": False,
            "error": "Classification failed.",
            "detail": str(e),
        }), 500


if __name__ == "__main__":
    host = os.environ.get("SENTINELCAT_HOST", "0.0.0.0")
    port = int(os.environ.get("SENTINELCAT_PORT", "8000"))
    app.run(host=host, port=port, debug=False)