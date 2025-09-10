import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator


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

movies: list[Movie] = []

class MovieCreate(BaseModel):
    """
    Sirve para consultar y registrar datos
    """
    # id: int | None = None  # Hacemos que sea int o None, opcional
    id: int = Field(gt=0, default=movies[-1].id + 1 if movies else 1)  # gt "greater than"
    titulo: str # Como tenemos la validacion abajo, ahora podemos eliminar esto = Field(min_length=1, max_length=100, example="El Padrino")
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
    
    @validator("titulo")
    def validate_title(cls, value):
        if len(value) < 1:
            raise ValueError("El campo 'título' no puede estar vacío")
        if len(value) > 100:
            raise ValueError("El campo 'título' no puede tener más de 100 caracteres")
        return value