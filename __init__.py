from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #Comm
  
@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")
  
@app.route('/paris/')
def meteo():
    response = urlopen('https://api.openweathermap.org/data/2.5/forecast/daily?q=Paris,fr&cnt=16&appid=bd5e378503939ddaee76f12ad7a97608')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('temp', {}).get('day') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
  
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def mongraphique2():
    return render_template("histogramme.html")

@app.route('/commits/')
def commits():
    url = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"
    r = requests.get(url)
    commits_data = r.json()
    
    # Extraction des minutes de chaque commit
    commit_minutes = {}
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        minute = datetime.strptime(commit_date, '%Y-%m-%dT%H:%M:%SZ').minute
        commit_minutes[minute] = commit_minutes.get(minute, 0) + 1

    # Création du graphique
    plt.figure(figsize=(10, 6))
    plt.bar(commit_minutes.keys(), commit_minutes.values(), color='blue')
    plt.xlabel('Minutes')
    plt.ylabel('Nombre de commits')
    plt.title('Commits par minute')

    # Sauvegarde du graphique en format base64 pour affichage dans HTML
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()

    return '<img src="data:image/png;base64,{}">'.format(plot_url)
  
if __name__ == "__main__":
  app.run(debug=True)
