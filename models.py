from sqlalchemy import Column, Integer, String, Float, Time, Date
from database import Base

class Actividad(Base):
    __tablename__ = "actividades"

    id_actividad = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)                     #el valor nullable significa si un campo puede ser null o no
    descripcion = Column(String(255), nullable=True)
    costo =  Column(Float, nullable=False)


class Turno(Base):
    __tablename__ = "turnos"

    id_turno = Column(Integer, primary_key=True, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)


class Alumno(Base):
    __tablename__ = "alumnos"

    ci_alumno = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    telefono = Column(String(15), nullable=True)
    correo = Column(String(255), nullable=False)


class Instructor(Base):
    __tablename__ = "instructores"

    ci_instructor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)