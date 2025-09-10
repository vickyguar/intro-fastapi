"""
Modelos de datos/ esquemas para la aplicación FastAPI
"""

from fastapi import FastAPI, Body, Path, Query
from pydantic import BaseModel, Field # Para validar campos
from typing import Optional #, List
import datetime

from fastapi.responses import JSONResponse, HTMLResponse, PlainTextResponse, RedirectResponse, FileResponse

# movies = [
#     {"id": 1, "titulo": "El Padrino", "anio": 1972, "genero": "Crimen"},
#     {"id": 2, "titulo": "Forrest Gump", "anio": 1994, "genero": "Drama"},
#     {"id": 3, "titulo": "Inception", "anio": 2010, "genero": "Ciencia Ficción"}
# ]

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
    return [movie.model_dump() for movie in movies] # Convertimos cada movie a diccionario



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

movies: list[Movie] = []

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


class MovieCreate(BaseModel):
    """
    Sirve para consultar y registrar datos
    """
    # id: int | None = None  # Hacemos que sea int o None, opcional
    id: int = Field(gt=0, default=movies[-1].id + 1 if movies else 1)  # gt "greater than"
    titulo: str = Field(min_length=1, max_length=100, example="El Padrino")
    anio: int = Field(le=datetime.date.today().year)  # le: less or equal, El año debe ser menor o igual al actual. gt "greater than"
    genero: str
    director: str = None
    duracion: int = None  # en minutos
    sinopsis: Optional[str]
    
    # Otra forma de añadir valores por defecto es extendiendo la configuracion del modelo
    # model_config pertenece al esquema gracias a BaseModel
    model_config = {
        "json_schema_extra": {
            "example": {
                # id se autogenera
                "titulo": "El Padrino",
                "anio": 1972,
                "genero": "Crimen",
                "director": "Francis Ford Coppola",
                "duracion": 175,
                "sinopsis": "La historia de la familia Corleone..."
            }
        }
    }


@app.post("/peliculas_model")
def create_movie_model(movie: MovieCreate):
    new_id = movies[-1].id + 1 if movies else 1
    # Creamos una nueva instancia con el id asignado
    movie.id = new_id
    movies.append(movie) # Como ya indicamos que es de tipo movie la lista de arriba
    # movies.append(movie.model_dump()) # Lo convertimos a diccionario porque lo necesita
    # movies.append(movie.dict()) # En Pydantic v2, está discontinuado
    # return {"message": "Película creada exitosamente", "movies": movies}
    return [movie.model_dump() for movie in movies] # Convertimos cada movie a diccionario
    #return RedirectResponse(url="/", status_code=303) # Redirigimos a la raiz para ver todas las peliculas


@app.put("/peliculas_model/{movie_id}")
def update_movie_model(movie_id: int, movie: MovieUpdate) -> list[Movie] | dict:
    for _, m in enumerate(movies):
        if m.id == movie_id:
            m.titulo = movie.titulo
            m.anio = movie.anio
            m.genero = movie.genero
            m.director = movie.director
            m.duracion = movie.duracion
            m.sinopsis = movie.sinopsis
            return [movie.model_dump() for movie in movies] # Convertimos cada movie a diccionario

    return {"message": "Película no encontrada"}


"""
Validación de datos con Pydantic
"""

# Pydantic automaticamente da validacines en algunos casos.
# Por ejemplo "Field required" si no se envía un campo obligatorio.
# Por ejemplo, si accedemos a un link invalido /peliculas/one en lugar de /peliculas/1

# Ahora cómo se hace para validar parametros de ruta y parámetros query?

@app.get("/peliculas/{id}")
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            return movie.model_dump() # Convertimos cada movie a diccionario
    return {"message": "Película no encontrada"}

# Ahora con los parámetros query

@app.get("/peliculas/")
def get_movies_by_category(category:str = Query(min_length=3, max_length=20)) -> list[Movie] | dict:
    results = []
    for movie in movies:
        if movie.genero.lower() == category.lower(): # Ignoramos mayusculas y minusculas
            results.append(movie.model_dump())
    if results:
        return results
    return {"message": "No se encontraron películas en esa categoría"}

"""
Otros tipos de respuestas.
El JSON response no es obligatorio utilizarlo, pero es común.
"""

@app.get("/peliculas")
def get_movies() -> JSONResponse:
    content=[movie.model_dump() for movie in movies]
    # Ejemplo con codigo de estado
    # Cuando obtenemos todas las películas, por defecto es 200 (OK)
    return JSONResponse(content=content, status_code=200)


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

"""