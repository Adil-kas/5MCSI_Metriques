from flask import Flask, render_template, jsonify, request
from urllib.request import urlopen
import requests
from datetime import datetime
import json

app = Flask(__name__)

# Page d'accueil
@app.route('/')
def hello_world():
    return render_template('hello.html')

# Page de contact (HTML)
@app.route("/contact/")
def contact():
    return render_template("contact.html")

# Traitement du formulaire contact
@app.route("/submit_contact/", methods=["POST"])
def submit_contact():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    message = request.form.get('message')
    return f"<h2>Merci {first_name} {last_name} pour votre message !</h2><p>{message}</p>"

# Exercice 3 : Données météo
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=b6907d289e10d714a6e88b30761fae22')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15  # Kelvin -> Celsius
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

# Page avec graphique météo
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

# Page avec histogramme météo
@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

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

# Route test : extraire minute depuis une date
@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

# Démarrage de l'application
if __name__ == "__main__":
    app.run(debug=True)



