from flask import Blueprint, render_template, request, redirect, url_for, session,jsonify
from tensorflow.keras.preprocessing import image
import numpy as np
import io
import os
import json
from .seguridad import cargar_clave_privada, cargar_clave_publica

from tensorflow.keras.models import load_model

from .get_data import get_new_data


API_KEY = "6609c948-c626-4ab4-8e09-f98420bdf2fd"


public_key = cargar_clave_publica("public_key.pem")
private_key = cargar_clave_privada("private_key.pem")

#model = load_model('model_x_ray.keras')


views = Blueprint('views',__name__)

def check_api_key(func):
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('API-Key')

        if provided_key == API_KEY:
            return func(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid API key'}), 401
    return wrapper


@views.route('/')
def home():
    return render_template("home.html")


@views.route("/test_siteWeb",methods=["GET"])
def test_siteWeb():
    return "Working"


@views.route("/get_new_model",methods=["POST"])
#@check_api_key
def save_model():
    data = request.get_json()

    get_new_data(data)

    return "Ha Guardado Perfectamente!"


#Get Result -POST Select-
def get_result(disease_type):
    save_dir = "saving_data"
    if disease_type == 1: 
        model_updated = load_model(os.path.join(save_dir, 'model_x_ray.keras'))
        with open(os.path.join(save_dir, "x_ray_data.json"), "r") as archivo:
            data = json.load(archivo)
    elif disease_type == 2: 
        model_updated = load_model(os.path.join(save_dir, 'model_brain_tumor.keras'))
        with open(os.path.join(save_dir, "brain_tumor_data.json"), "r") as archivo:
            data = json.load(archivo)
    elif disease_type == 3: 
        model_updated = load_model(os.path.join(save_dir, 'model_melanoma.keras'))
        with open(os.path.join(save_dir, "melanoma_data.json"), "r") as archivo:
            data = json.load(archivo)

    imagen_archivo = request.files['image']

    imagen_bytes = imagen_archivo.read()
    #print(data)
    X  = []
    img = image.load_img(io.BytesIO(imagen_bytes), target_size=[int(data["img_size"]), int(data["img_size"])], color_mode = 'grayscale')
    X.append(image.img_to_array(img))
    X = np.array(X)

    predictions = model_updated.predict(X)
    y_pred_int = predictions.argmax(axis=1)
    max_pri = np.max((predictions))
    max_pri = max_pri * 100
    print(max_pri)

    pre_result = "tt"
    if disease_type == 1: 
        for i,v in enumerate(y_pred_int):
            if(v == 0): pre_result = "NORMAL"
            elif (v == 1): pre_result = "BACTERIA"
            else: pre_result = "VIRUS"

    elif disease_type == 2: 
        for i,v in enumerate(y_pred_int):
            if(v == 0): pre_result = "GLIOMA"
            elif (v == 1): pre_result = "MENINGIOMA"
            elif (v == 2): pre_result = "NOTUMOR"
            else: pre_result = "PITUITARY"

    elif disease_type == 3: 
        for i,v in enumerate(y_pred_int):
            if(v == 0): pre_result = "NEVUS"
            elif (v == 1): pre_result = "MELANOMA"
            else: pre_result = "SEBORRHEIC KERATOSIS"

    return pre_result, str(max_pri.round(2))
    
@views.route('/selectxray', methods=['POST'])
def select_image_x_ray_post():
    if request.method == 'POST':
        pre_result, pred_value =  get_result(1)

        session['result'] = pre_result
        session['value'] = pred_value
        #print(roc_auc)
        return redirect(url_for('views.result_image_x_ray', dato=pre_result))
        
    return render_template("select_x_ray.html")

@views.route('/selectbrain_tumor', methods=['POST'])
def select_image_brain_tumor_post():
    if request.method == 'POST':
        pre_result,pred_value =  get_result(2)

        session['result'] = pre_result
        session['value'] = pred_value
        #print(roc_auc)
        return redirect(url_for('views.result_image_brain_tumor', dato=pre_result))
        
    return render_template("select_image_brain_tumor.html")

@views.route('/selectmelanoma', methods=['POST'])
def select_image_melanoma_post():
    if request.method == 'POST':
        pre_result,pred_value =  get_result(3)
        

        session['result'] = pre_result
        session['value'] = pred_value
        #print(roc_auc)
        return redirect(url_for('views.result_image_melanoma', dato=pre_result))
        
    return render_template("select_melanoma.html")



#GET select disease ----------------------------------------------
@views.route('/selectxray', methods=['GET'])
def select_image_x_ray_get():
    save_dir = "saving_data"
    with open(os.path.join(save_dir, "x_ray_data.json"), "r") as archivo:
        data = json.load(archivo)
    return render_template("select_x_ray.html",general_data=data)

@views.route('/selectbrain_tumor', methods=['GET'])
def select_image_brain_tumor_get():
    save_dir = "saving_data"
    with open(os.path.join(save_dir, "brain_tumor_data.json"), "r") as archivo:
        data = json.load(archivo)
    return render_template("select_brain_tumor.html",general_data=data)

@views.route('/selectmelanoma', methods=['GET'])
def select_image_melanoma_get():
    save_dir = "saving_data"
    with open(os.path.join(save_dir, "melanoma_data.json"), "r") as archivo:
        data = json.load(archivo)
    return render_template("select_melanoma.html",general_data=data)



#Show Result ----------------------------------------------------------------
@views.route('/resultxray')
def result_image_x_ray():
    data = {
        "result" : session.get('result', None),
        "value" : session.get('value', None)
    } 
    return render_template("result_x_ray.html", result_data=data)

@views.route('/resultbrain_tumor')
def result_image_brain_tumor():
    data = {
        "result" : session.get('result', None),
        "value" : session.get('value', None)
    }
    return render_template("result_brain_tumor.html", result_data=data)

@views.route('/resultmelanoma')
def result_image_melanoma():
    data = {
        "result" : session.get('result', None),
        "value" : session.get('value', None)
    }
    return render_template("result_melanoma.html", result_data=data)

