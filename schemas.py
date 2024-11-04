from pydantic import BaseModel, Field
from datetime import time


class TurnoPost(BaseModel):
    hora_inicio: time
    hora_fin: time

class ActividadPost(BaseModel):
    nombre: str
    descripcion: str
    costo: float


#estructura que se utiliza para la respuesta al cliente
class ActividadResponse(BaseModel):
    id_actividad: int
    nombre: str
    descripcion: str
    costo: float

#estructura de los campos en la solicitud para actualizar una actividad
class ActividadUpdate(BaseModel):
    nombre: str = Field(None, max_length=100)
    descripcion: str = Field(None, max_length=255)
    costo: float = Field(None, gt=0)