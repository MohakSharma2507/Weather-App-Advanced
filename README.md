# Weather App - Advanced

## Overview

Weather App - Advanced is a Flask-based web application that allows users to search, view, and store weather information. The app uses the OpenWeatherMap API for weather data and SQLAlchemy with SQLite for persistent storage. It also integrates with the YouTube Data API to display relevant weather videos.

## Features

- Search current weather by location
- Display 5-day forecast (12:00 PM data points)
- Save current weather data to a local SQLite database
- View search history with date, temperature, and description
- Filter stored records by date
- Re-fetch historical entries
- Delete individual stored records
- Embedded YouTube video forecast based on location and date

## Technologies Used

- Python (Flask)
- Flask-SQLAlchemy
- SQLite
- HTML/CSS (Bootstrap 5)
- OpenWeatherMap API
- YouTube Data API

## Folder Structure

Weather-App-Advanced/
├── app.py                  # Main application logic
├── models.py               # SQLAlchemy database model
├── requirements.txt        # Project dependencies
├── static/
│   └── style.css           # Custom styles
├── templates/
│   ├── index.html          # Main weather interface
│   └── history.html        # History page
├── instance/
│   └── weather.db          # SQLite database
└── .env                    # API keys and config (not pushed)

## Author

**Mohak Sharma**  
[LinkedIn – PM Accelerator](https://www.linkedin.com/company/product-manager-accelerator)
