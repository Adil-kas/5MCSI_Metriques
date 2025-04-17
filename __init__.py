from flask import Flask, render_template, jsonify
from urllib.request import urlopen
from datetime import datetime
import json

app = Flask(__name__)

# Route principale : page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

# Exercice 2 : route /contact/
@app.route('/contact/')
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

# Exercice 3 : route /tawarano/
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=b6907d289e10d714a6e88b30761fae22')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Conversion Kelvin -> Celsius
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

if __name__ == "__main__":
    app.run(debug=True)
