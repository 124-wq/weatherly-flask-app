from flask import Blueprint, request, jsonify
from models import db, WeatherRecord
from services.weather_service import get_weather

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/weather", methods=["GET"])
def fetch_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    weather_data = get_weather(city)

    if not weather_data:
        return jsonify({"error": "City not found"}), 404

    # Save to DB
    record = WeatherRecord(
        location=weather_data["location"],
        temperature=weather_data["temperature"],
        description=weather_data["description"],
        humidity=weather_data["humidity"]
    )

    db.session.add(record)
    db.session.commit()

    return jsonify(weather_data)

@weather_bp.route("/records", methods=["GET"])
def get_records():
    records = WeatherRecord.query.all()

    result = []

    for record in records:
        result.append({
            "id": record.id,
            "location": record.location,
            "temperature": record.temperature,
            "description": record.description,
            "humidity": record.humidity,
            "created_at": record.created_at
        })

    return jsonify(result)

@weather_bp.route("/records/<int:id>", methods=["PUT"])
def update_record(id):
    record = WeatherRecord.query.get(id)

    if not record:
        return jsonify({"error": "Record not found"}), 404

    data = request.json

    if "location" in data:
        record.location = data["location"]

    if "temperature" in data:
        record.temperature = data["temperature"]

    if "description" in data:
        record.description = data["description"]

    if "humidity" in data:
        record.humidity = data["humidity"]

    db.session.commit()

    return jsonify({"message": "Record updated successfully"})

@weather_bp.route("/records/<int:id>", methods=["DELETE"])
def delete_record(id):
    record = WeatherRecord.query.get(id)

    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Record deleted successfully"})

import pandas as pd
from flask import send_file
import io

@weather_bp.route("/export/csv", methods=["GET"])
def export_csv():
    records = WeatherRecord.query.all()

    if not records:
        return jsonify({"error": "No records found"}), 404

    data = []

    for record in records:
        data.append({
            "id": record.id,
            "location": record.location,
            "temperature": record.temperature,
            "description": record.description,
            "humidity": record.humidity,
            "created_at": record.created_at
        })

    df = pd.DataFrame(data)

    output = io.StringIO()
    df.to_csv(output, index=False)
    output.seek(0)

    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype="text/csv",
        as_attachment=True,
        download_name="weather_records.csv"
    )