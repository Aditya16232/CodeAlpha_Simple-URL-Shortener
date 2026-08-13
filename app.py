import secrets
import sqlite3

from flask import Flask, jsonify, redirect, render_template, request

import database

app = Flask(__name__)

ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
CODE_LENGTH = 6
MAX_COLLISION_RETRIES = 5


def generate_short_code():
    return "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))


def create_short_code(long_url):
    for _ in range(MAX_COLLISION_RETRIES):
        code = generate_short_code()
        try:
            database.insert_url(code, long_url)
            return code
        except sqlite3.IntegrityError:
            continue
    raise RuntimeError("Failed to generate a unique short code")


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/shorten")
def shorten():
    data = request.get_json(silent=True) or {}
    long_url = (data.get("long_url") or "").strip()

    if not long_url:
        return jsonify({"error": "long_url is required"}), 400
    if not (long_url.startswith("http://") or long_url.startswith("https://")):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    short_code = create_short_code(long_url)

    short_url = request.host_url.rstrip("/") + "/" + short_code
    return jsonify(
        {
            "short_code": short_code,
            "short_url": short_url,
            "long_url": long_url,
        }
    ), 200


@app.route("/<short_code>")
def redirect_to_long_url(short_code):
    long_url = database.get_url(short_code)
    if long_url is None:
        return render_template("404.html", short_code=short_code), 404
    return redirect(long_url, code=302)


if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)