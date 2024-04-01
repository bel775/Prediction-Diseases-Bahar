from flask import Blueprint, render_template, request, redirect, url_for, session
import time
import requests
import base64
from .seguridad import cifrar_datos, descifrar_datos, cargar_clave_privada, cargar_clave_publica


api_key = "6609c948-c626-4ab4-8e09-f98420bdf2fd"


public_key = cargar_clave_publica("public_key.pem")
private_key = cargar_clave_privada("private_key.pem")

views = Blueprint('views',__name__)

@views.route('/')
def home():
    return render_template("home.html")


@views.route('/selectxray', methods=['GET','POST'])
def select_imagen_x_ray():
    if request.method == 'POST':
        imagen = request.form.get('imageInput')
        #imagen = "virus"
        
        imagen_cifrados = cifrar_datos(imagen,public_key)
        imagen_cifrado_base64 = base64.b64encode(imagen_cifrados).decode('utf-8')
        
        url = "https://localhost:1998/respuesta"

        datos = {
            "imagen": imagen_cifrado_base64
        }

        headers = {
            "Content-Type": "application/json",
            "API-Key": api_key
        }

        respuesta = requests.get(url, json=datos, headers=headers, verify='certificado_autofirmado.pem')

        if respuesta.status_code == 200:
            data = respuesta.json()
            datos_cifrados_base64 = data.get('result', '')
            datos_cifrados = base64.b64decode(datos_cifrados_base64)
            datos = descifrar_datos(datos_cifrados,private_key)
            dato = datos
            session['result'] = dato
            return redirect(url_for('views.result_imagen_x_ray', dato=dato))

        else:
            print(f"Error en la solicitud: {respuesta.status_code}")
            print(respuesta.text)
            return render_template("select_x_ray.html")
        
    return render_template("select_x_ray.html")


@views.route('/selectmelanoma')
def select_imagen_melanoma():
    return render_template("select_melanoma.html")

@views.route('/resultxray')
def result_imagen_x_ray():
    dato = session.get('result', None)  # Obtener el dato de la sesión de Flask
    return render_template("result_x_ray.html", dato=dato)

