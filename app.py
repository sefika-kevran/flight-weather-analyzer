from flask import Flask, request, render_template, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")
print("API_KEY:", API_KEY)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
def weather():
    city = request.args.get("city", "").strip()

    if not city:
        return jsonify({"error": "Sehir girilmedi"}), 400

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        msg = data.get("message", "Bilinmeyen hata")
        if "Invalid API key" in msg:
            msg = "API key henuz aktif degil veya gecersiz. Biraz sonra tekrar dene."
        return jsonify({"error": msg}), response.status_code

    city_name = data["name"].replace(" Province", "").replace(" District", "")

    temp = data["main"]["temp"]
    wind = data["wind"]["speed"]
    status = "Uygun" if wind < 10 else "Riskli"

    return jsonify({
        "city": city_name,
        "temperature": temp,
        "wind_speed": wind,
        "flight_status": status
    })

if __name__ == "__main__":
    app.run(debug=True)
    