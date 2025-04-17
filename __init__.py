from flask import Flask, render_template, jsonify, request
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
def contact():
    return render_template("contact.html")

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

# Formulaire de contact : route pour soumettre les données
@app.route("/submit_contact/", methods=["POST"])
def submit_contact():
    # Récupération des données envoyées par l'utilisateur via le formulaire
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    message = request.form.get('message')

    # Afficher un message avec les informations envoyées
    return f"<h2>Merci {first_name} {last_name} pour votre message !</h2><p>{message}</p>"

from datetime import datetime

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

import requests

@app.route('/commits/')
def commits():
    # Récupérer les commits depuis l'API GitHub
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    # Liste pour stocker le nombre de commits par minute
    commits_per_minute = {}

    # Parcourir tous les commits et extraire les minutes
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        minute = extract_minutes(commit_date)['minutes']

        if minute in commits_per_minute:
            commits_per_minute[minute] += 1
        else:
            commits_per_minute[minute] = 1

    # Convertir les données pour les afficher dans un graphique
    data = [{'minute': minute, 'commits': count} for minute, count in commits_per_minute.items()]

    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
