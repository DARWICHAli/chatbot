from flask import Flask, render_template, request
import json
from ordonnanceur import Ordonnanceur
from random import randrange

app = Flask(__name__)

ordo = None
hist = None
lock_hist = None

@app.before_first_request
def start():
    global lock_hist
    global ordo
    global hist
    ordo = Ordonnanceur()
    hist = []
    lock_hist = []

@app.route('/', methods = ['POST', 'GET'])
def index():
    global lock_hist
    if request.method == 'POST':
        sdt = [request.form.get('sd'), request.form.get('st')]
        edt = [request.form.get('ed'), request.form.get('et')]
        lock_hist.append([sdt, edt])
    return render_template('index.html')

@app.route('/calendar')
def calendar():
    return render_template('calendar.html')

@app.route('/postmethod', methods = ['POST'])
def get_post_javascript_data():
    global ordo
    global hist
    jsdata = request.form['javascript_data']
    # Traitement NLP
    
    # Sending data to UI
    nb_pages = randrange(4000, 10000)
    result = ordo.add_creneau(nb_pages)
    if result[0] == -1:
        response = {'flask_data': f"Something is wrong : {result[1]}"}
    else:
        hist.append(result)
        response = {'flask_data': f"Done : you can find your query in the calendar ! Take care. ! Nb Pages : {nb_pages}"}
    
    return json.dumps(response)

@app.route('/ready', methods = ['POST'])
def ready():
    global hist
    jsdata = request.form['ready']
    response = {'ready': hist}
    return json.dumps(response)

@app.route('/lock', methods = ['POST'])
def lock():
    global lock_hist
    jsdata = request.form['lock']
    response = {'lock': lock_hist}
    return json.dumps(response)

if __name__ == '__main__':
    app.run(debug=True)