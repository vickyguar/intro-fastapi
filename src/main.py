"""
Ejemplo de aplicación con FastAPI:
- Definición de modelos y validaciones con Pydantic
- Inclusión de routers y middlewares personalizados
- Manejo de diferentes tipos de respuestas (JSON, texto plano, archivos, redirecciones)
- Personalización de códigos de estado y documentación de la API
"""

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse, FileResponse
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler # mi middleware personalizado para manejar errores

app = FastAPI()

# Incluir rutas
app.include_router(prefix="/movies", router=movie_router)

# middleware personalizado para manejo de errores
app.add_middleware(HTTPErrorHandler)


@app.get("/")
def read_root() -> PlainTextResponse:
    return PlainTextResponse(content="Mi primera API con FastAPI!")


@app.get("/get_file")
def get_file():
    return FileResponse("example.pdf")


# movies = [
#     {"id": 1, "titulo": "El Padrino", "anio": 1972, "genero": "Crimen"},
#     {"id": 2, "titulo": "Forrest Gump", "anio": 1994, "genero": "Drama"},
#     {"id": 3, "titulo": "Inception", "anio": 2010, "genero": "Ciencia Ficción"}
# ]