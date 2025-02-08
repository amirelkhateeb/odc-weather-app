from flask import Flask, render_template, request, jsonify
import requests
import sqlite3
import os

app = Flask(__name__)

# Replace with your OpenWeatherMap API key
API_KEY = "your_openweathermap_api_key"

# SQLite database path
DATABASE = "weather.db"

# Initialize the database
def init_db():
    if not os.path.exists(DATABASE):
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE weather (
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
            CREATE TABLE settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                last_searched_city TEXT
            )
        ''')
        conn.commit()
        conn.close()

# Save last searched city to settings table
def save_last_searched_city(city):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO settings (id, last_searched_city) VALUES (1, ?)', (city,))
    conn.commit()
    conn.close()

# Get last searched city from settings table
def get_last_searched_city():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT last_searched_city FROM settings WHERE id = 1')
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

@app.route("/")
def home():
    # Retrieve the last searched city to pre-fill the search form
    last_searched_city = get_last_searched_city()
    return render_template("index.html", last_searched_city=last_searched_city)

@app.route("/weather", methods=["GET"])
def get_weather():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    # Check if weather data for this city is already in the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM weather WHERE city = ? ORDER BY fetched_at DESC LIMIT 1", (city,))
    cached_data = c.fetchone()
    conn.close()

    if cached_data:
        # Return cached data if available
        return jsonify({
            "name": cached_data[1],
            "sys": {"country": cached_data[2]},
            "main": {"temp": cached_data[3]},
            "weather": [{"main": cached_data[4], "description": cached_data[4], "icon": cached_data[5]}]
        })

    # Fetch data from OpenWeatherMap API if not cached
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "City not found"}), 404

    data = response.json()

    # Save the fetched weather data to the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        INSERT INTO weather (city, country, temperature, description, icon)
        VALUES (?, ?, ?, ?, ?)
    ''', (data["name"], data["sys"]["country"], data["main"]["temp"], data["weather"][0]["description"], data["weather"][0]["icon"]))
    conn.commit()
    conn.close()

    # Save the last searched city
    save_last_searched_city(city)

    return jsonify({
        "name": data["name"],
        "sys": {"country": data["sys"]["country"]},
        "main": {"temp": data["main"]["temp"]},
        "weather": [{"main": data["weather"][0]["main"], "description": data["weather"][0]["description"], "icon": data["weather"][0]["icon"]}]
    })

@app.route("/cities", methods=["GET"])
def get_cities():
    # Retrieve all cities from the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT * FROM weather ORDER BY fetched_at DESC")
    cities = c.fetchall()
    conn.close()

    # Format the data for frontend
    city_list = []
    for city in cities:
        city_list.append({
            "city": city[1],
            "country": city[2],
            "temperature": city[3],
            "description": city[4],
            "icon": city[5]
        })
    
    return jsonify(city_list)

@app.route("/delete_city", methods=["POST"])
def delete_city():
    city = request.json.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    # Delete the city from the database
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM weather WHERE city = ?", (city,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"City {city} deleted successfully!"})

if __name__ == "__main__":
    init_db()  # Initialize the database when the app starts
    app.run(debug=True, host="0.0.0.0", port=5000)