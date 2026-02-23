from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    city = db.Column(db.String(100))
    country = db.Column(db.String(10))

    temperature = db.Column(db.Float)
    description = db.Column(db.String(200))
    humidity = db.Column(db.Integer)

    wind_speed = db.Column(db.Float)
    feels_like = db.Column(db.Float)
    pressure = db.Column(db.Integer)

    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)