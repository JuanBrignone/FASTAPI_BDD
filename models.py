from sqlalchemy import Column, Integer, String, Float
from database import Base

class Actividad(Base):
    __tablename__ = "actividades"

    id_actividad = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), nullable=False)                     #el valor nullable significa si un campo puede ser null o no
    descripcion = Column(String(255), nullable=True)
    costo =  Column(Float, nullable=False)


