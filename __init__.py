from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
from urllib.request import Request, urlopen

                                                                                                                                       
app = Flask(__name__)  

@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')#gguyfyfy
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)
@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")
@app.route("/histogramme/")
def histogramme():
    
  return render_template("histogramme.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})




GITHUB_API_URL = "https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits"

def fetch_all_commits(per_page=100, max_pages=10, token=None):
    commits = []
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    page = 1
    while page <= max_pages:
        url = f"{GITHUB_API_URL}?per_page={per_page}&page={page}"
        resp = requests.get(url, headers=headers)
        if resp.status_code != 200:
            break
        data = resp.json()
        if not isinstance(data, list) or not data:
            break
        commits.extend(data)
        page += 1
    return commits

def minute_key_from_date(date_str):
    # date_str example: "2024-02-11T11:57:27Z"
    dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    return dt.strftime('%Y-%m-%dT%H:%MZ')  # précision à la minute

def aggregate_commits_by_minute(commits):
    counts = defaultdict(int)
    for c in commits:
        try:
            date_str = c['commit']['author']['date']
        except (KeyError, TypeError):
            continue
        minute_key = minute_key_from_date(date_str)
        counts[minute_key] += 1
    # Transformer en liste triée
    result = [{"minute": k, "count": v} for k, v in sorted(counts.items())]
    return result

@app.route('/commits/')
def commits_graph():
    # Option A: récupérer sur tout le repo
    commits = fetch_all_commits(per_page=100, max_pages=5)  # ajuste selon besoin
    data = aggregate_commits_by_minute(commits)
    return jsonify(data)


 


  
if __name__ == "__main__":
  app.run(debug=True)
