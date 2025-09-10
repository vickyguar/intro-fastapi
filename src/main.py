"""
Modelos de datos/ esquemas para la aplicación FastAPI
"""

from fastapi import FastAPI, Body, Path, Query, APIRouter
from pydantic import validator, BaseModel, Field # Para validar campos
from typing import Optional #, List
import datetime
from src.routers.movie_router import movie_router
from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse

# movies = [
#     {"id": 1, "titulo": "El Padrino", "anio": 1972, "genero": "Crimen"},
#     {"id": 2, "titulo": "Forrest Gump", "anio": 1994, "genero": "Drama"},
#     {"id": 3, "titulo": "Inception", "anio": 2010, "genero": "Ciencia Ficción"}
# ]

app = FastAPI()


"""
Incluimos las rutas ahora
"""

app.include_router(prefix="/movies", router=movie_router)


# Que pasaría si quisieramos guardar más información de la película?
# Por ejemplo, el director, duración, sinopsis, etc.
# Podríamos agregar más parámetros a la función, pero se volvería engorroso.
# En su lugar, podemos definir un modelo de datos usando Pydantic.


# Podríamos crear un nuevo esquema que se use únicamente para
# actualizar datos. Esto sería lo más ideal.

"""
Validación de datos con Pydantic
"""

# Pydantic automaticamente da validacines en algunos casos.
# Por ejemplo "Field required" si no se envía un campo obligatorio.
# Por ejemplo, si accedemos a un link invalido /peliculas/one en lugar de /peliculas/1

# Ahora cómo se hace para validar parametros de ruta y parámetros query?


"""
Otros tipos de respuestas.
El JSON response no es obligatorio utilizarlo, pero es común.
"""


# También existen las respuestas de texto plano:
@app.get("/")
def read_root() -> PlainTextResponse:
    return PlainTextResponse(content = "Mi primera API con FastAPI!")


@app.get("/get_file")
def get_file():
    return FileResponse("example.pdf")

"""
Códigos de estado
Se pueden cambiar dentro de JSONResponse o cualquier otro tipo de respuesta.

El código de estado que modificamos en ese caso es el codigo de estado que enviamos
en la respuesta al cliente.

Hay otro codigo de estado que podemos cambiar que tiene que ver con la
documentacion de la API.

"""

"""
Ahora vamos a ver cómo extender las validaciones que usamos anteriormente usando Pydantic.
"""