from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend


def cifrar_datos(datos, public_key):
    cifrado = public_key.encrypt(
        datos.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cifrado

def descifrar_datos(cifrado,private_key):
    datos_descifrados = private_key.decrypt(
        cifrado,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return datos_descifrados.decode('utf-8')

def cargar_clave_privada(ruta_archivo):
    with open(ruta_archivo, 'rb') as f:
        clave_privada = serialization.load_pem_private_key(
            f.read(),
            password=None,  # Si la clave está protegida por contraseña, proporciona la contraseña aquí
            backend=default_backend()
        )
    return clave_privada

def cargar_clave_publica(ruta_archivo):
    with open(ruta_archivo, 'rb') as f:
        clave_publica = serialization.load_pem_public_key(
            f.read(),
            backend=default_backend()
        )
    return clave_publica