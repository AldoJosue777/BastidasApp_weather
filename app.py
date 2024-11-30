from flask import Flask, render_template, request
import requests

app = Flask(__name__)


API_KEY = "5d4acc5cc26056ce9f3c2a7e014ceadc"
API_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route("/", methods=["GET", "POST"])
def index():
    weather_data = None
    error = None

    if request.method == "POST":
        ciudad = request.form.get("ciudad")
        if not ciudad:
            error = "Por favor, ingresa una ciudad."
        else:
            try:
                params = {
                    "q": ciudad,
                    "appid": API_KEY,
                    "units": "metric",
                    "lang": "es"
                }
                response = requests.get(API_URL, params=params)
                response.raise_for_status()
                data = response.json()
                weather_data = {
                    "ciudad": data["name"],
                    "temperatura": round(data["main"]["temp"], 1),
                    "descripcion": data["weather"][0]["description"].capitalize(),
                    "latitud": abs(data["coord"]["lat"]),
                    "longitud": abs(data["coord"]["lon"])
                }
            except requests.exceptions.HTTPError:
                error = f"No se encontró la ciudad: {ciudad}. Intenta de nuevo."
            except Exception as err:
                error = "Ocurrió un error. Intenta nuevamente."

    return render_template("index.html", weather_data=weather_data, error=error)

@app.route("/cv.html")
def cv():
    return render_template("cv.html")


if __name__ == "__main__":
    app.run(debug=True)

