import os
import time
import sys

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

API_KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
if not API_KEY:
    sys.exit(
        "Error: GOOGLE_PLACES_API_KEY not set. "
        "Create leads/.env from leads/.env.example and add your key."
    )

TEXT_SEARCH_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
DETAILS_FIELDS = "name,formatted_address,formatted_phone_number,website,url"

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/search", methods=["POST"])
def search():
    body = request.get_json(silent=True) or {}
    query = (body.get("query") or "").strip()
    if not query:
        return jsonify({"error": "query is required"}), 400

    places = []
    next_page_token = None

    for page in range(3):
        try:
            if next_page_token:
                params = {"pagetoken": next_page_token, "key": API_KEY}
                time.sleep(2)
            else:
                params = {"query": query, "key": API_KEY}

            resp = requests.get(TEXT_SEARCH_URL, params=params, timeout=10)
            data = resp.json()
        except Exception as e:
            return jsonify({"error": str(e), "status": "REQUEST_FAILED"}), 502

        status = data.get("status")
        if status == "ZERO_RESULTS" and page == 0:
            return jsonify({"places": [], "count": 0, "status": "ZERO_RESULTS"})
        if status not in ("OK", "ZERO_RESULTS"):
            return jsonify({"error": data.get("error_message", status), "status": status}), 502

        for place in data.get("results", []):
            places.append({
                "place_id": place.get("place_id"),
                "name": place.get("name", ""),
                "address": place.get("formatted_address", ""),
                "rating": place.get("rating"),
            })

        next_page_token = data.get("next_page_token")
        if not next_page_token:
            break

    return jsonify({"places": places, "count": len(places), "status": "OK"})


@app.route("/api/details", methods=["POST"])
def details():
    body = request.get_json(silent=True) or {}
    place_ids = body.get("place_ids") or []
    if not place_ids:
        return jsonify({}), 200

    result = {}
    for pid in place_ids:
        try:
            resp = requests.get(
                DETAILS_URL,
                params={"place_id": pid, "fields": DETAILS_FIELDS, "key": API_KEY},
                timeout=10,
            )
            data = resp.json()
        except Exception:
            result[pid] = {"phone": "", "website": "", "maps_url": ""}
            continue

        place = data.get("result", {})
        result[pid] = {
            "phone": place.get("formatted_phone_number", ""),
            "website": place.get("website", ""),
            "maps_url": place.get("url", ""),
        }

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
