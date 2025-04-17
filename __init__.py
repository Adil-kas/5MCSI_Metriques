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


@app.route('/commits/')
def affichecommits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

    try:
        response = urlopen(url)
        raw_data = response.read()
        data = json.loads(raw_data.decode("utf-8"))
    except Exception as e:
        return f"Erreur lors de l'appel à l'API GitHub : {e}"

    minutes_list = []
    for commit in data:
        try:
            date_str = commit.get("commit", {}).get("author", {}).get("date")
            if date_str:
                date_obj = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
                minutes_list.append(date_obj.strftime('%H:%M'))
        except Exception as e:
            print(f"Erreur: {e}")

    if not minutes_list:
        return "Aucun commit valide trouvé."

    # 🧠 Tri chronologique
    minute_counts = Counter(minutes_list)
    sorted_items = sorted(minute_counts.items(), key=lambda x: datetime.strptime(x[0], "%H:%M"))
    minutes = [item[0] for item in sorted_items]
    counts = [item[1] for item in sorted_items]

    return render_template("commits.html", minutes=minutes, counts=counts)
if __name__ == "__main__":
    app.run(debug=True)
