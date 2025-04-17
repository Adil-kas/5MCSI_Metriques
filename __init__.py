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
    
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
    
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")
    
@app.route("/contact/")
def contact():
    return render_template("contact.html")
from flask import request

from flask import request

from flask import request

@app.route("/submit_contact/", methods=["POST"])
def submit_contact():
    # Récupération des données envoyées par l'utilisateur via le formulaire
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    message = request.form.get('message')
    
    # Afficher un message avec les informations envoyées
    return f"<h2>Merci {first_name} {last_name} pour votre message !</h2><p>{message}</p>"

if __name__ == "__main__":
    app.run(debug=True)
