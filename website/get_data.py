from .seguridad import descifrar_datos, cargar_clave_privada
import json
import base64
import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow import keras
import os


private_key = cargar_clave_privada("private_key.pem")

def get_new_data(data):
    model_base64 = data.get('model', '')
    weights_base64 = data.get('weights', '')
    roc_auc_cifrado_base64 = data.get('roc_auc', '')
    loss_cifrado_base64 = data.get('loss', '')
    accuracy_cifrado_base64 = data.get('accuracy', '')
    disease_type_cifrado_base64 = data.get('disease_type', '')
    img_size_cifrado_base64 = data.get('img_size', '')
    balance_type_cifrado_base64 = data.get('balance_type', '')
    model_type_cifrado_base64 = data.get('model_type', '')
    activation_cifrado_base64 = data.get('activation', '')
    training_type_cifrado_base64 = data.get('training_type', '')
    batch_size_cifrado_base64 = data.get('batch_size', '')
    epochs_cifrado_base64 = data.get('epochs', '')
    optimization_cifrado_base64 = data.get('optimization', '')

    # Decode and decrypt model and weights
    model_json = base64.b64decode(model_base64).decode('utf-8')
    weights_json = base64.b64decode(weights_base64).decode('utf-8')

    model = model_from_json(model_json) #model_base64
    weights_as_lists = json.loads(weights_json)
    weights = [np.array(w) for w in weights_as_lists]
    model.set_weights(weights)

    # Decode and decrypt additional parameters
    roc_auc_cifrado = base64.b64decode(roc_auc_cifrado_base64)
    loss_cifrado = base64.b64decode(loss_cifrado_base64)
    accuracy_cifrado = base64.b64decode(accuracy_cifrado_base64)
    disease_type_cifrado = base64.b64decode(disease_type_cifrado_base64)
    img_size_cifrado = base64.b64decode(img_size_cifrado_base64)
    balance_type_cifrado = base64.b64decode(balance_type_cifrado_base64)
    model_type_cifrado = base64.b64decode(model_type_cifrado_base64)
    activation_cifrado = base64.b64decode(activation_cifrado_base64)
    training_type_cifrado = base64.b64decode(training_type_cifrado_base64)
    batch_size_cifrado = base64.b64decode(batch_size_cifrado_base64)
    epochs_cifrado = base64.b64decode(epochs_cifrado_base64)
    optimization_cifrado = base64.b64decode(optimization_cifrado_base64)

    # Decrypt values
    roc_auc = descifrar_datos(roc_auc_cifrado, private_key)
    loss = descifrar_datos(loss_cifrado, private_key)
    accuracy = descifrar_datos(accuracy_cifrado, private_key)
    disease_type = descifrar_datos(disease_type_cifrado, private_key)
    img_size = descifrar_datos(img_size_cifrado, private_key)
    balance_type = descifrar_datos(balance_type_cifrado, private_key)
    model_type = descifrar_datos(model_type_cifrado, private_key)
    activation = descifrar_datos(activation_cifrado, private_key)
    training_type = descifrar_datos(training_type_cifrado, private_key)
    batch_size = descifrar_datos(batch_size_cifrado, private_key)
    epochs = descifrar_datos(epochs_cifrado, private_key)
    optimization = descifrar_datos(optimization_cifrado, private_key)

    balance_type_str = "Neither"
    if balance_type == "1": balance_type_str = "OverSampler"
    elif balance_type == "2": balance_type_str = "UnderSampler"

    model_type_str = ""
    if model_type == "1": model_type_str = "Functional API"
    elif model_type == "2": model_type_str = "Sequential API"
    elif model_type == "3": model_type_str = "SubClassing"
    elif model_type == "4": model_type_str = "Hybrid"
    elif model_type == "5": model_type_str = "ResNet"
    elif model_type == "6": model_type_str = "EfficientNet"
    elif model_type == "7": model_type_str = "VGG16"
    elif model_type == "8": model_type_str = "AlexNet"
    else: model_type_str = "None"
    
    training_type_str = ""
    if training_type == "1": training_type_str = "Normal Train"
    elif training_type == "2": training_type_str = "Image Data Generator"
    # Prepare data dictionary
    jason_data = {
        "roc_auc": float(roc_auc),
        "loss": float(loss),
        "accuracy": float(accuracy),
        "img_size": img_size,
        "balance_type": balance_type_str,
        "model_type": model_type_str,
        "activation": activation,
        "training_type": training_type_str,
        "batch_size": batch_size,
        "epochs": epochs,
        "optimization": optimization
    }
    
    save_dir = "saving_data"  # Corrected path to avoid issues with root directory
    os.makedirs(save_dir, exist_ok=True)

    #model_file_path = os.path.join(save_dir, "received_model.keras")
    #uploaded_file.save(model_file_path)

    #model = keras.models.load_model(model_file_path)
    print(disease_type)
    if disease_type == "1":
        print("GG")
        model.save(os.path.join(save_dir, 'model_x_ray.keras'))
        with open(os.path.join(save_dir, "x_ray_data.json"), "w") as archivo:
            json.dump(jason_data, archivo)
    elif disease_type == "2":
        model.save(os.path.join(save_dir, 'model_brain_tumor.keras'))
        with open(os.path.join(save_dir, "brain_tumor_data.json"), "w") as archivo:
            json.dump(jason_data, archivo)
    elif disease_type == "3":
        model.save(os.path.join(save_dir, 'model_melanoma.keras'))
        with open(os.path.join(save_dir, "melanoma_data.json"), "w") as archivo:
            json.dump(jason_data, archivo)

    
