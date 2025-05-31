from flask import Flask, render_template, request, redirect, url_for
import requests
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# Load environment variables
load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv('OPENWEATHER_API_KEY')
YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(100), nullable=False)

def get_weather_data(location):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def get_forecast_data(location):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric"
    return requests.get(url).json()

def filter_forecast_by_noon(forecast_list):
    return [entry for entry in forecast_list if "12:00:00" in entry["dt_txt"]]

def get_youtube_video(location):
    today = datetime.now().strftime('%B %d, %Y')
    query = f"{location} weather forecast {today}"
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        q=query,
        part='snippet',
        maxResults=1,
        type='video',
        order='date'
    )
    response = request.execute()
    if response['items']:
        video_id = response['items'][0]['id']['videoId']
        return f"https://www.youtube.com/embed/{video_id}"
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    forecast_data = None
    video_url = None
    location = ""
    error_message = None
    condition = "default"

    if request.method == "POST":
        location = request.form.get("location")

        if location:
            weather_data = get_weather_data(location)
            forecast_raw = get_forecast_data(location)

            if weather_data.get("cod") != 200:
                error_message = weather_data.get("message", "Invalid location or API error")
            else:
                forecast_data = filter_forecast_by_noon(forecast_raw.get("list", []))
                condition = weather_data["weather"][0]["main"].lower()
                video_url = get_youtube_video(location)

                # Store current weather only
                temperature = weather_data['main']['temp']
                description = weather_data['weather'][0]['description']
                record = WeatherRecord(location=location, temperature=temperature, description=description)
                db.session.add(record)
                db.session.commit()

    return render_template("index.html", weather=weather_data, forecast=forecast_data,
                           location=location, error=error_message, condition=condition,
                           video_url=video_url)

@app.route("/history", methods=["GET", "POST"])
def history():
    records = WeatherRecord.query.order_by(WeatherRecord.date.desc()).limit(10).all()

    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                end = datetime.strptime(end_date, "%Y-%m-%d")
                records = WeatherRecord.query.filter(WeatherRecord.date.between(start, end)).order_by(WeatherRecord.date.desc()).all()
            except ValueError:
                pass

    return render_template("history.html", records=records)

@app.route("/refetch/<int:record_id>")
def refetch(record_id):
    record = WeatherRecord.query.get_or_404(record_id)
    return render_template("index.html", 
        weather={
            'main': {'temp': record.temperature, 'humidity': 'N/A'},
            'wind': {'speed': 'N/A'},
            'weather': [{'description': record.description, 'icon': '10d'}]
        },
        forecast=None,
        location=record.location,
        condition=record.description.split()[0].lower() if record.description else "default",
        video_url=None,
        error=None,
        stored_weather=WeatherRecord.query.order_by(WeatherRecord.date.desc()).all()
    )

@app.route("/delete/<int:id>")
def delete(id):
    record = WeatherRecord.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for("history"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=5050)