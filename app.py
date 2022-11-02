from flask import Flask, render_template, request
import json
from ordonnanceur import Ordonnanceur
from random import randrange
import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import tensorflow_text
from tensorflow import keras
import spacy
from googletrans import Translator


app = Flask(__name__)

ordo = None
hist = None
lock_hist = None
model_b = None
model_s = None
model_t = None

def check_week_clear():
    global lock_hist
    global ordo
    global hist
    now = datetime.datetime.now()
    print("Checking ...")
    if now.weekday() == 0:
        ordo = Ordonnanceur()
        hist = []
        lock_hist = []
        print("Done ! Schedule Reset.")
    return 0



def start():
    global lock_hist
    global ordo
    global hist
    ordo = Ordonnanceur()
    hist = []
    lock_hist = []

    # Chargement des deux modèles:
    global model_b
    global model_s
    global model_t
    print("Loading Translation Model ...")
    model_t = Translator()
    print("Model Translation Loaded")
    print("Loading Model Bert ....")
    model_b = keras.models.load_model('./static/model/model-classifier')
    print("Model Bert Loaded")
    print("Loading Model Spacy ...")
    model_s = spacy.load("./static/model/model-extraction")
    print("Model Spacy Loaded")
    



@app.route('/', methods = ['POST', 'GET'])
def index():
    global lock_hist
    global ordo
    if request.method == 'POST':
        sdt = [request.form.get('sd'), request.form.get('st')]
        edt = [request.form.get('ed'), request.form.get('et')]
        ordo.bloque_hour(sdt, edt)
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
    global model_t
    global model_b
    global model_s

    #Translation ...
    translated_text = (model_t.translate(jsdata, dest='en')).text

    print(f"Translated Text: {translated_text}")
    #Classification + Extraction
    y_pred_c = model_b.predict([translated_text])
    print(f"Classifier : {y_pred_c}")
    if y_pred_c[0] < 0.5:
        response = {'flask_data': "Something is wrong : Your request is not accepted make sure to precise the name of the document and the number of pages"}
    else:
        # Sending data to UI
        doc = model_s(translated_text)
        print(f'Extraction : {doc.ents}')
        nb_pages = -1
        for ent in doc.ents:
            if ent.label_ == "DocName":
                nb_pages = int(ent.text)
                break
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
    scheduler = BackgroundScheduler(daemon = True)
    scheduler.start()
    trigger = CronTrigger(
        year="*", month="*", day="*", hour="0", minute="1"
    )
    scheduler.add_job(
        check_week_clear,
        trigger=trigger
    )
    start()
    app.run(debug=True)