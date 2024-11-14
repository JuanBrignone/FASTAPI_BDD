from pydantic import BaseModel, Field
from datetime import time, date
from typing import Optional


class AlumnoPost(BaseModel):
    ci_alumno: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    telefono: str
    correo: str
    contraseña: str

class LoginPost(BaseModel):
    correo: str
    contraseña: str
    ci_alumno: int

class InstructorPost(BaseModel):
    ci_instructor: int
    nombre: str
    apellido: str


class TurnoPost(BaseModel):
    hora_inicio: time
    hora_fin: time

class ActividadPost(BaseModel):
    nombre: str
    descripcion: str
    costo: float


#estructura que se utiliza para la respuesta al cliente (respuesta en postman)
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


class AlumnoResponse(BaseModel):
    ci_alumno: int
    nombre: str
    apellido: str
    fecha_nacimiento: date
    telefono: str
    correo: str


class LoginRequest(BaseModel):
    correo: str
    contraseña: str

class LoginResponse(BaseModel):
    message: str


class ClaseCreate(BaseModel):
    ci_instructor: int
    id_actividad: int
    id_turno: int
    dictada: Optional[bool] = False

class ClaseResponse(BaseModel):
    id_clase: int
    nombre_actividad: str
    nombre_instructor: str 
    hora_inicio: time
    hora_fin: time
    costo_actividad: int

class AlumnoClaseRequest(BaseModel):
    id_clase: int
    ci_alumno: int
    id_equipamiento: Optional[int]

class EquipamientoPost(BaseModel):
    id_actividad: int
    nombre: str
    descripcion: Optional[str]
    costo: float

class EquipamientoResponse(BaseModel):
    nombre_actividad: str
    nombre_equipamiento: str
    descripcion_equipamiento: str
    costo_equipamiento: float


class EquipamientoResponseActividad(BaseModel):
    id_equipamiento: int
    nombre: str
    descripcion: str
    costo: float


