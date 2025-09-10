# Pongo los endpoints aca
from fastapi import FastAPI, Body, Path, Query, APIRouter
from fastapi.responses import JSONResponse
from src.models.movie_models import Movie, MovieCreate, MovieUpdate, movies

movie_router = APIRouter()

@movie_router.post("/peliculas_model")
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


@movie_router.put("/{movie_id}")
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


@movie_router.get("/{id}")
def get_movie(id: int = Path(gt=0)) -> Movie | dict:
    for movie in movies:
        if movie.id == id:
            content = movie.model_dump() # Convertimos cada movie a diccionario
            return JSONResponse(content=content, status_code=200)
    return JSONResponse(content={"message": "Película no encontrada"}, status_code=404)


# Ahora con los parámetros query
@movie_router.get("/")
def get_movies_by_category(category:str = Query(min_length=3, max_length=20)) -> list[Movie] | dict:
    results = []
    for movie in movies:
        if movie.genero.lower() == category.lower(): # Ignoramos mayusculas y minusculas
            results.append(movie.model_dump())
    if results:
        return results
    return {"message": "No se encontraron películas en esa categoría"}


@movie_router.get("/", tags=["Películas"], status_code=200, response_description="Esto debe devolver una respuesta exitosa") # 500 SOLO PARA COMPROBAR QUE SE ESTE MODIFICANDO
def get_movies() -> JSONResponse:
    #content=[movie.model_dump() for movie in movies]
    # Ejemplo con codigo de estado
    # Cuando obtenemos todas las películas, por defecto es 200 (OK)
    # Asi podemos modificar el código de error que queremos eviar 
    # cuando respondemos una peticion a un cliente
    # =====================================================================
    return # JSONResponse(content=content, status_code=200) # TODO: NOTE: No me tira el middleware, revisar


@movie_router.post("/")
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

