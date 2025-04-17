from flask import Flask, render_template, jsonify, request
import requests
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

# Route HTML du graphique de commits
@app.route("/commits/")
def commits_graph():
    return render_template("commits.html")

# API JSON pour les données de commits
@app.route("/api/commits/")
def commits_data():
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'
    response = requests.get(url)
    commits_data = response.json()

    commits_per_minute = {}

    for commit in commits_data:
        try:
            commit_date = commit['commit']['author']['date']
            minute = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').minute
            commits_per_minute[minute] = commits_per_minute.get(minute, 0) + 1
        except:
            continue  # Juste au cas où certaines données sont mal formées

    data = [{'minute': k, 'commits': v} for k, v in sorted(commits_per_minute.items())]
    return jsonify(data)

# Démarrage de l'application
if __name__ == "__main__":
    app.run(debug=True)
