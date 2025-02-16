import os
import requests
import sqlite3
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Get API key from environment variable
API_KEY = ("ffaffa61c2c7b8aaec11fe62b1f386f7")
DATABASE = "weather.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Create tables
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            temperature REAL NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            fetched_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            last_searched_city TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_last_searched_city(city):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO settings (id, last_searched_city) VALUES (1, ?) ON CONFLICT(id) DO UPDATE SET last_searched_city = excluded.last_searched_city', (city,))
    conn.commit()
    conn.close()

def get_last_searched_city():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT last_searched_city FROM settings WHERE id = 1')
    result = c.fetchone()
    conn.close()
    return result[0] if result and result[0] is not None else ""

@app.route("/")
def home():
    return render_template("index.html", last_searched_city=get_last_searched_city())

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("""
        SELECT * FROM weather 
        WHERE city = ? 
        AND fetched_at >= datetime('now', '-10 minutes')
        ORDER BY fetched_at DESC 
        LIMIT 1
    """, (city,))
    cached_data = c.fetchone()
    conn.close()

    if cached_data:
        return jsonify({
            "name": cached_data[1],
            "sys": {"country": cached_data[2]},
            "main": {"temp": cached_data[3]},
            "weather": [{"main": cached_data[4], "description": cached_data[3], "icon": cached_data[5]}]
        })

    if not API_KEY:
        return jsonify({"error": "API key is missing"}), 500

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = response.json()

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO weather (city, country, temperature, description, icon)
        VALUES (?, ?, ?, ?, ?)
    ''', (data["name"], data["sys"]["country"], data["main"]["temp"], data["weather"][0]["description"], data["weather"][0]["icon"]))
    conn.commit()
    conn.close()

    save_last_searched_city(city)

    return jsonify({
        "name": data["name"],
        "sys": {"country": data["sys"]["country"]},
        "main": {"temp": data["main"]["temp"]},
        "weather": [{"main": data["weather"][0]["main"], "description": data["weather"][0]["description"], "icon": data["weather"][0]["icon"]}]
    })

@app.route("/cities", methods=["GET"])
def get_cities():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT city, country, temperature, description, icon FROM weather ORDER BY fetched_at DESC")
    cities = c.fetchall()
    conn.close()

    return jsonify([
        {"city": city[0], "country": city[1], "temperature": city[2], "description": city[3], "icon": city[4]}
        for city in cities
    ])

@app.route("/delete_city", methods=["POST"])
def delete_city():
    city = request.json.get("city")
    if not city or not city.isalpha():
        return jsonify({"error": "Invalid city name"}), 400

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM weather WHERE city = ?", (city,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"City {city} deleted successfully!"})

if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)