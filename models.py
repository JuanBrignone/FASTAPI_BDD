from sqlalchemy import Column, Integer, String, Float, Time, Date, ForeignKey, Boolean
from database import Base
from sqlalchemy.orm import relationship

class Actividad(Base):
    __tablename__ = "actividades"

    id_actividad = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)                     #el valor nullable significa si un campo puede ser null o no
    descripcion = Column(String(255), nullable=True)
    costo =  Column(Float, nullable=False)

    clases = relationship("Clase", back_populates="actividad")


class Turno(Base):
    __tablename__ = "turnos"

    id_turno = Column(Integer, primary_key=True, index=True)
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)

    clases = relationship("Clase", back_populates="turno")


class Alumno(Base):
    __tablename__ = "alumnos"

    ci_alumno = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    telefono = Column(String(15), nullable=True)
    correo = Column(String(255), nullable=False)
    contraseña = Column(String(255), nullable=False)

    login = relationship("Login", back_populates="alumno")


class Login(Base):
    __tablename__ = "login"
    correo = Column(String(255), primary_key=True, index=True)
    contraseña = Column(String(255), nullable=False)
    ci_alumno = Column(Integer, ForeignKey('alumnos.ci_alumno'), nullable=False)

    alumno = relationship("Alumno", back_populates="login")



class Instructor(Base):
    __tablename__ = "instructores"

    ci_instructor = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    clases = relationship("Clase", back_populates="instructor")



class Clase(Base):
    __tablename__ = "clase"
    id_clase = Column(Integer, primary_key=True, autoincrement=True)
    ci_instructor = Column(String, ForeignKey("instructores.ci_instructor"))
    id_actividad = Column(Integer, ForeignKey("actividades.id_actividad"))
    id_turno = Column(Integer, ForeignKey("turnos.id_turno"))
    dictada = Column(Boolean)

    instructor = relationship("Instructor", back_populates="clases")
    actividad = relationship("Actividad", back_populates="clases")
    turno = relationship("Turno", back_populates="clases")