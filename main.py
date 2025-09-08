"""
Modelos de datos/ esquemas para la aplicación FastAPI
"""

from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Optional #, List

movies = [
    {"id": 1, "titulo": "El Padrino", "anio": 1972, "genero": "Crimen"},
    {"id": 2, "titulo": "Forrest Gump", "anio": 1994, "genero": "Drama"},
    {"id": 3, "titulo": "Inception", "anio": 2010, "genero": "Ciencia Ficción"}
]

app = FastAPI()

@app.post("/peliculas")
def create_movie(
    id: int=Body(),
    titulo: str=Body(),
    anio: int=Body(),
    genero: str=Body()
):
    movies.append({
        "id": id, 
        "titulo": titulo, 
        "anio": anio, 
        "genero": genero
        })
    return {"message": "Película creada exitosamente", "movies": movies}


# Que pasaría si quisieramos guardar más información de la película?
# Por ejemplo, el director, duración, sinopsis, etc.
# Podríamos agregar más parámetros a la función, pero se volvería engorroso.
# En su lugar, podemos definir un modelo de datos usando Pydantic.


class Movie(BaseModel):
    """
    Sirve para consultar y registrar datos
    """
    id: int | None = None  # Hacemos que sea int o None, opcional
    titulo: str
    anio: int
    genero: str
    director: str = None
    duracion: int = None  # en minutos
    sinopsis: Optional[str]

# Podríamos crear un nuevo esquema que se use únicamente para
# actualizar datos. Esto sería lo más ideal.

class MovieUpdate(BaseModel):
    """
    Sirve únicamente para actualizar datos.
    Notar que no se envia el id
    """
    titulo: Optional[str] = None
    anio: Optional[int] = None
    genero: Optional[str] = None
    director: Optional[str] = None
    duracion: Optional[int] = None  # en minutos
    sinopsis: Optional[str] = None


@app.post("/peliculas_model")
def create_movie_model(movie: Movie):
    movies.append(movie.model_dump()) # Lo convertimos a diccionario porque lo necesita
    # movies.append(movie.dict()) # En Pydantic v2, está discontinuado
    return {"message": "Película creada exitosamente", "movies": movies}


@app.put("/peliculas_model/{movie_id}")
def update_movie_model(movie_id: int, movie: MovieUpdate) -> list[Movie] | dict:
    for _, m in enumerate(movies):
        if m["id"] == movie_id:
            movies["titulo"] = movie.titulo
            movies["anio"] = movie.anio
            movies["genero"] = movie.genero
            movies["director"] = movie.director
            movies["duracion"] = movie.duracion
            movies["sinopsis"] = movie.sinopsis
            return movies
    return {"message": "Película no encontrada"}
