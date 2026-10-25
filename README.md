# Evidencia GA7-220501096-AA5-EV01
## Diseño y desarrollo de servicios web - caso

**Aprendiz:** Yerson Valera Sierra
**Programa:** Tecnología en Análisis y Desarrollo de Software (ADSO) - SENA

## Descripción

Servicio web (API REST) desarrollado en **Python + Flask** que permite:

1. **Registrar** un usuario (usuario + contraseña).
2. **Iniciar sesión** validando las credenciales:
   - Si son correctas → `"Autenticación satisfactoria"`
   - Si son incorrectas → `"Error en la autenticación"`

## Requisitos

- Python 3.9 o superior
- pip

## Instalación y ejecución

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Ejecutar el servicio
python app.py
```

El servicio quedará disponible en: `http://127.0.0.1:5000`

## Endpoints

### 1. Registro de usuario
`POST /api/registro`

**Body (JSON):**
```json
{
  "usuario": "yerson",
  "contrasena": "12345"
}
```

### 2. Inicio de sesión
`POST /api/login`

**Body (JSON):**
```json
{
  "usuario": "yersonValera",
  "contrasena": "12345"
}
```

**Respuesta si es correcta:**
```json
{
  "estado": "exitoso",
  "mensaje": "Autenticación satisfactoria."
}
```

**Respuesta si es incorrecta:**
```json
{
  "estado": "error",
  "mensaje": "Error en la autenticación."
}
```

### 3. Listar usuarios registrados (prueba)
`GET /api/usuarios`

## Pruebas con cURL

```bash
# Registrar usuario
curl -X POST http://127.0.0.1:5000/api/registro -H "Content-Type: application/json" -d "{\"usuario\":\"yersonValera\",\"contrasena\":\"12345\"}"

# Iniciar sesión correctamente
curl -X POST http://127.0.0.1:5000/api/login -H "Content-Type: application/json" -d "{\"usuario\":\"yersonValera\",\"contrasena\":\"12345\"}"

# Iniciar sesión con contraseña incorrecta
curl -X POST http://127.0.0.1:5000/api/login -H "Content-Type: application/json" -d "{\"usuario\":\"yerson\",\"contrasena\":\"clave errada\"}"
```

## Control de versiones

Este proyecto fue versionado con **Git** y publicado en **GitHub**.
Ver el enlace del repositorio en el archivo `enlace_repositorio.txt`.
