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
from numerizer import numerize
from keras import backend as K

def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    return true_positives / (possible_positives + K.epsilon())

def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    return true_positives / (predicted_positives + K.epsilon())

def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))

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



def init_models_jobs():

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
    model_b = keras.models.load_model('./static/model/model-classifier', custom_objects = {"recall_m": recall_m, "precision_m": precision_m, "f1_m": f1_m})
    print("Model Bert Loaded")
    print("Loading Model Spacy ...")
    model_s = spacy.load("./static/model/model-extraction")
    print("Model Spacy Loaded")

    scheduler = BackgroundScheduler(daemon = True)
    scheduler.start()
    trigger = CronTrigger(
        year="*", month="*", day="*", hour="0", minute="1"
    )
    scheduler.add_job(
        check_week_clear,
        trigger=trigger
    )
    



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

@app.route('/clear_calendar')
def clear_calendar():
    global ordo
    global hist
    global lock_hist
    ordo = Ordonnanceur()
    hist = []
    lock_hist = []
    print("Done ! Schedule Reset.")
    return render_template('index.html')


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
        nb_pages = next((int(numerize(ent.text)) for ent in doc.ents if ent.label_ == "NbPages"), -1)
        doc_name = next((ent.text for ent in doc.ents if ent.label_ == "DocName"), -1)
        if doc_name == -1 or nb_pages == -1:
            response = {'flask_data': "Something is wrong : Your request is not accepted make sure to precise the name of the document and the number of pages"}
        else:    
            result = ordo.add_creneau(nb_pages)

            if result[0] == -1:
                response = {'flask_data': f"Something is wrong : {result[1]}"}
            else:
                hist.append(result)
                response = {'flask_data': f"Done : you can find your query in the calendar ! Take care. ! Nb Pages : {nb_pages}, Document Name : {doc_name}"}

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
    init_models_jobs()
    app.run(debug=True, use_reloader=False)