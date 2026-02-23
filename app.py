from flask import Flask, render_template,request
from config import Config
from models import db, WeatherRecord
from routes.weather_routes import weather_bp
from services.weather_service import get_weather
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
app.register_blueprint(weather_bp)

@app.route("/")
def home():
    weather = None
    city = request.args.get("city")

    if city:
        weather = get_weather(city)

        if weather:
            record = WeatherRecord(
                city=weather["city"],  
                temperature=weather["temperature"],
                description=weather["description"],
                humidity=weather["humidity"],
                latitude=weather["latitude"],
                longitude=weather["longitude"]
            )

            db.session.add(record)
            db.session.commit()

    return render_template("index.html", weather=weather)

@app.route("/history")
def history():
    records = WeatherRecord.query.order_by(WeatherRecord.created_at.desc()).limit(10).all()
    return render_template("history.html", records=records)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)