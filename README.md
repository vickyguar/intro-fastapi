# Introducción a FastAPI

Notas y práctica del curso [FastAPI](https://www.youtube.com/watch?v=OKUDmlvB8Hk&list=PLHftsZss8mw7pSRpCyd-TM4Mu43XdyB3R).

---

## ¿Qué es una API?

Una **interfaz** es una capa de abstracción que permite que dos sistemas se comuniquen. Gracias a esta capa, podemos interactuar con un sistema sin necesidad de conocer lo que ocurre en su interior.

Una **API** (*Application Programming Interface* o *Interfaz de Programación de Aplicaciones*) es una interfaz que permite que distintas aplicaciones o programas de software intercambien datos entre sí.

## Conceptos iniciales

- **Arquitectura de software**: es la forma en que está diseñado un sistema. Define cómo se organizan los componentes, cómo se comunican y qué funciones cumplen.
- **Servicio web**: sistema que permite la comunicación entre equipos dentro de una red, generalmente usando estándares como **HTTP**.
- **REST (Representational State Transfer)**: arquitectura para el diseño de servicios web.  
  - En español: *Transferencia de Estado Representacional*.  
  - Características principales:
    - El estado no se envía en las peticiones (es *stateless*).  
    - Se pueden almacenar respuestas en caché.  
    - El servidor define qué datos están disponibles y cómo se pueden manipular.  
- **Formato de datos más usado**: `JSON` (*JavaScript Object Notation*). Ligero, fácil de leer y ampliamente soportado.  

## Tipos de APIs

| Tipo        | Descripción                                                                 |
|-------------|-----------------------------------------------------------------------------|
| **Locales** | Se ejecutan en el mismo entorno (ej. API interna de un programa).           |
| **Remotas** | Permiten la comunicación vía servicios web. Los más comunes son:            |
|             | - **REST** → el más usado.                                                  |
|             | - **SOAP** → protocolo más estricto y basado en XML, usado en entornos más corporativos. |

Además, las APIs pueden ser:  

- **Públicas** → acceso abierto a cualquiera.  
- **Privadas** → requieren autenticación.  

En APIs privadas, al autenticarte el servidor devuelve un **token** que contiene los datos de autenticación.  
El formato más común es **JWT (JSON Web Token)**.

## Recursos y endpoints

Cada recurso que consultamos en una API tiene un identificador único llamado **URI**.  
La consulta se hace a través de un **endpoint** (la URL expuesta por la API).  

## Códigos de respuesta HTTP

Cuando solicitas información a través de una API, el servidor responde con un código de estado:

| Categoría  | Código  | Significado                                       |
|------------|---------|---------------------------------------------------|
| ✅ **2xx** | 200, 201 | Éxito.                                           |
| 🔄 **3xx** | 301, 302 | Redirecciones.                                   |
| ❌ **4xx** | 400, 403, 404 | Error del cliente (solicitud inválida, sin autorización, recurso no encontrado). |
| ⚠️ **5xx** | 500, 503 | Error en el servidor.                            |

## Métodos HTTP

Los métodos HTTP permiten interactuar con los recursos de la API.  
Son equivalentes a un **CRUD** (*Create, Read, Update, Delete*) en bases de datos:

| Método  | Acción                                   |
|---------|------------------------------------------|
| **GET**    | Consultar información                  |
| **POST**   | Crear un nuevo recurso                 |
| **PUT**    | Actualizar información existente       |
| **DELETE** | Eliminar un recurso                    |

---

# Pydantic

Una de las grandes desventajas de Python es la falta de tipado estático. Python usa tipado dinámico, lo que significa que cuando creas una variable, no hay que especificarle el tipo.

Por ejemplo:
```
# Python
x = 10
x = "hello" # hasta podes sobreescribir con otro tipo

// En C
int x = 10;
```

Esto, accidentalmente puede hacer que crees un objeto inválido:
```
alice = Person("Alice", 24) # Correct
alice = Person("Alice", "24") # Mistake
```

Para resolver este tipo de problemas, actualmente Python tiene dataclasses y type-hinting.
```
@dataclass
class Person:
  name: str
  age: int
```

Usando Pydantic:
```
from pydantic import BaseModel

class User(BaseModel):
  name: str
  email: str
  acount_id: int
```

→ Entonces, Pydantic es una **librería de validación de datos**.

Para instanciar un usuario se puede hacer:
```
user = User(
  name="Vicky"
  email="vicky@guar.com"
  acount_id=1
)
```

También se puede con un diccionario de la siguiente manera:
```
user_data = {
  name="Vicky"
  email="vicky@guar.com"
  acount_id=1
}

user = User(**user_data)
```

Se pueden crear, además, validaciones customizadas de la siguiente manera (es una class function):
```
@validator("acount_id")
def validate_acount_id(cls, value):
  if value <= 0:
    raise ValueError(f"account_id must be positive: {value}")
  return value
```

Pydantic también facilita la **JSON serialization**: 
- Para convertir un modelo de Pydantic a JSON, se puede hacer simplemente `user_json_str = user.json()`. 
- Si no queres un JSON string, pero queres un diccionario de python podes hacer: `user_json_obj = user.dict()`.
- Para volver al modelo Pydantic podes hacer: `json_str = {"name": "jack", "email": "jack@test.io", "account_id": 1234}´´`, y luego `user = User.parse_raw(json_str)`

### Comparacion con dataclass
|                 | pydantic | dataclass  |
|-----------------|----------|------------|
| Type Hints      | ✅       | ✅        |
| Data validation | ✅       | ❌        |
| Serialization   | ✅       | ⚠️        |
|  Built-In       | ❌       | ✅        |

---

# Notitas al margen

### Archivo init
- **Archivo  `__init__.py `**: está ubicado en la carpeta src/routers del repo. Este archivo convierte la carpeta en un paquete de Python. `init` es la abreviatura de *initialization*. Se pueden incluir variables. Cuando se importa el paquete, se corre todo lo que está en el `__init__.py`.

Por ejemplo, si tenes una estructura de carpetas que es la siguiente:
```
ejemplo-init
|-- main.py
|-- math_operations
|  |-- __init__.py
|  |-- addition.py
|  |-- substraction.py
```

En el archivo __init__.py se puede poner:
```
from .addition import add
from .substraction import sub
```

Y las implementaciones en el main cambian en cada caso:
<table>
  <thead>
    <tr>
      <th>Con <code>__init__.py</code></th>
      <th>Sin <code>__init__.py</code></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>
<pre><code>import math_operations
result = math_operations.add(5, 3)</code></pre>
      </td>
      <td>
<pre><code>import math_operations
import math_operations.addition
result = math_operations.addition.add(5, 3)</code></pre>
      </td>
    </tr>
  </tbody>
</table>

→ Lo que se puede hacer en el `__init__.py` es crear un string connection, por ejemplo.

### Tipo de dato EmailStr
`from pydantic import EmailStr`: sirve para validar que los emails sean válidos.
