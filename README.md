
# Weather-App-Advanced

This project is submitted for **Tech Assessment 2: Weather App (Advanced)** as part of the AI Engineer Intern – AI/ML/GenAI Application at PM Accelerator.

## Overview

This advanced weather app builds on top of the initial assessment and focuses on implementing full **CRUD functionality**, **API integrations**, and data persistence using **Flask** and **SQLite**. It enables users to input locations, fetch current weather data, store it, and manage historical records with options to view, update, delete, or re-fetch weather data.

## Key Features

### Full CRUD Implementation (Using SQLite + SQLAlchemy)

- **Create:**  
  - When a user searches for weather in a location, the app stores the temperature, condition, location, and timestamp in a SQLite database.

- **Read:**  
  - A separate `/history` page lists all previously searched weather entries, ordered by most recent.
  - Users can optionally filter these records by date or re-fetch the weather view for any specific record.

- **Update:**  
  - Although not exposed via UI, the backend is structured to support record updates (editable via model).

- **Delete:**  
  - Users can delete specific records directly from the history page.

### Input Validation

- Validates location by checking API response.
- Ensures user doesn’t enter empty or malformed data.

### API Integrations

- **OpenWeatherMap API:**  
  Fetches real-time weather and 5-day forecast based on location.

- **YouTube Data API:**  
  Embeds the latest weather-related video for the searched location and current date.

## Technologies Used

- Python (Flask)
- Flask-SQLAlchemy
- SQLite
- Bootstrap 5 (HTML/CSS)
- OpenWeatherMap API
- YouTube Data API

## Folder Structure

```
Weather-App-Advanced/
├── app.py               # Main Flask application
├── models.py            # Database model (SQLAlchemy)
├── requirements.txt     # Dependencies
├── static/
│   └── style.css        # Custom styles
├── templates/
│   ├── index.html       # Main weather interface
│   └── history.html     # Historical weather viewer
├── instance/
│   └── weather.db       # SQLite database file
└── .env                 # API credentials (excluded from version control)
```

## Author

**Mohak Sharma**  
[LinkedIn – PM Accelerator](https://www.linkedin.com/company/product-manager-accelerator)
