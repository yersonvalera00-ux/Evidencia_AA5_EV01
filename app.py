"""
Evidencia GA7-220501096-AA5-EV01
Diseño y desarrollo de servicios web - caso.

Servicio web (API REST) para REGISTRO e INICIO DE SESIÓN de usuarios.

Tecnología: Python 3 + Flask
Autor: Yerson Valera Sierra
Programa: Tecnología en Análisis y Desarrollo de Software (ADSO) - SENA

Descripción del caso:
- El servicio recibe un usuario y una contraseña.
- Si la autenticación es correcta, responde con un mensaje de
  "autenticación satisfactoria".
- Si la autenticación es incorrecta, responde con un mensaje de
  "error en la autenticación".
"""

# ---------------------------------------------------------
# 1. IMPORTACIÓN DE LIBRERÍAS
# ---------------------------------------------------------
from flask import Flask, request, jsonify  # Flask: framework para crear el servicio web
import hashlib                              # hashlib: para encriptar (hashear) las contraseñas

# ---------------------------------------------------------
# 2. CREACIÓN DE LA APLICACIÓN FLASK
# ---------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------
# 3. "BASE DE DATOS" EN MEMORIA
# ---------------------------------------------------------
# Para esta evidencia usamos un diccionario de Python como almacenamiento
# temporal de usuarios (en un proyecto real esto sería una base de datos
# como MySQL, PostgreSQL, etc.).
# Estructura: { "usuario": "contraseña_encriptada" }
usuarios_registrados = {}


# ---------------------------------------------------------
# 4. FUNCIÓN AUXILIAR: ENCRIPTAR CONTRASEÑA
# ---------------------------------------------------------
def encriptar_contrasena(contrasena):
    """
    Recibe una contraseña en texto plano y devuelve su versión
    encriptada usando el algoritmo SHA-256.
    Nunca se debe guardar una contraseña en texto plano.
    """
    return hashlib.sha256(contrasena.encode("utf-8")).hexdigest()


# ---------------------------------------------------------
# 5. ENDPOINT: REGISTRO DE USUARIO
# ---------------------------------------------------------
@app.route("/api/registro", methods=["POST"])
def registro():
    """
    Recibe un JSON con 'usuario' y 'contrasena'.
    Registra al usuario si no existe previamente.
    """
    # Obtenemos los datos enviados en formato JSON desde el cliente (Postman, front-end, etc.)
    datos = request.get_json(silent=True)

    # Validamos que llegaron los datos y que contienen los campos requeridos
    if not datos or "usuario" not in datos or "contrasena" not in datos:
        return jsonify({
            "estado": "error",
            "mensaje": "Debe enviar 'usuario' y 'contrasena' en el cuerpo de la petición."
        }), 400  # 400 = Bad Request

    usuario = datos["usuario"].strip()
    contrasena = datos["contrasena"]

    # Validamos que el usuario no esté vacío
    if usuario == "" or contrasena == "":
        return jsonify({
            "estado": "error",
            "mensaje": "El usuario y la contraseña no pueden estar vacíos."
        }), 400

    # Verificamos si el usuario ya existe
    if usuario in usuarios_registrados:
        return jsonify({
            "estado": "error",
            "mensaje": "El usuario ya se encuentra registrado."
        }), 409  # 409 = Conflict

    # Guardamos el usuario con la contraseña encriptada
    usuarios_registrados[usuario] = encriptar_contrasena(contrasena)

    return jsonify({
        "estado": "exitoso",
        "mensaje": "Usuario registrado correctamente."
    }), 201  # 201 = Created


# ---------------------------------------------------------
# 6. ENDPOINT: INICIO DE SESIÓN (LOGIN)
# ---------------------------------------------------------
@app.route("/api/login", methods=["POST"])
def login():
    """
    Recibe un JSON con 'usuario' y 'contrasena'.
    Valida las credenciales contra lo almacenado en 'usuarios_registrados'.
    - Si son correctas -> mensaje de autenticación satisfactoria.
    - Si son incorrectas -> mensaje de error en la autenticación.
    """
    datos = request.get_json(silent=True)

    # Validamos que llegaron los datos necesarios
    if not datos or "usuario" not in datos or "contrasena" not in datos:
        return jsonify({
            "estado": "error",
            "mensaje": "Debe enviar 'usuario' y 'contrasena' en el cuerpo de la petición."
        }), 400

    usuario = datos["usuario"].strip()
    contrasena = datos["contrasena"]

    # Encriptamos la contraseña recibida para compararla con la almacenada
    contrasena_encriptada = encriptar_contrasena(contrasena)

    # Verificamos si el usuario existe y si la contraseña coincide
    if usuario in usuarios_registrados and usuarios_registrados[usuario] == contrasena_encriptada:
        # Autenticación correcta
        return jsonify({
            "estado": "exitoso",
            "mensaje": "Autenticación satisfactoria."
        }), 200  # 200 = OK
    else:
        # Usuario no existe o la contraseña no coincide
        return jsonify({
            "estado": "error",
            "mensaje": "Error en la autenticación."
        }), 401  # 401 = Unauthorized


# ---------------------------------------------------------
# 7. ENDPOINT ADICIONAL: LISTAR USUARIOS (solo para pruebas / demostración)
# ---------------------------------------------------------
@app.route("/api/usuarios", methods=["GET"])
def listar_usuarios():
    """
    Devuelve la lista de usuarios registrados (sin mostrar las contraseñas).
    Útil para verificar el funcionamiento durante las pruebas.
    """
    return jsonify({
        "usuarios_registrados": list(usuarios_registrados.keys())
    }), 200


# ---------------------------------------------------------
# 8. PUNTO DE ENTRADA DE LA APLICACIÓN
# ---------------------------------------------------------
if __name__ == "__main__":
    # debug=True permite ver los errores detallados mientras se desarrolla
    # host="0.0.0.0" permite probar desde Postman/navegador en el mismo equipo
    app.run(debug=True, host="0.0.0.0", port=5000)
