from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Actividad, Turno, Alumno, Base
from schemas import TurnoPost, ActividadPost, ActividadResponse, ActividadUpdate, AlumnoPost

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#############################################################################################
#                               ACTIVIDADES                                                 #
#############################################################################################

#Trae todas las actividades
@app.get("/actividades")
async def read_actividades(db: Session = Depends(get_db)):
    actividades = db.query(Actividad).all()
    if not actividades:
        raise HTTPException(status_code=404, detail="No hay actividades disponibles")
    return actividades

#Agregar actividades
@app.post("/actividades")
async def post_actividad(actividad: ActividadPost, db: Session = Depends(get_db)):
    nueva_actividad = Actividad(
        nombre=actividad.nombre, 
        descripcion=actividad.descripcion,
        costo=actividad.costo
        )
    db.add(nueva_actividad)
    db.commit()
    db.refresh(nueva_actividad)
    return nueva_actividad


#Eliminar actividades
@app.delete("/actividades/{id_actividad}", status_code=200)
async def delete_actividad(id_actividad: int, db:Session = Depends(get_db)):
    actividad = db.query(Actividad).filter(Actividad.id_actividad == id_actividad).first()
    if not actividad:
        raise HTTPException(status_code=404, detail="No se encontro un turno para eliminar")
    db.delete(actividad)
    db.commit()
    return {"detail": "Actividad eliminada correctamente"}


#Modificar actividad
@app.put("/actividades/{id_actividad}", response_model=ActividadResponse)
async def update_actividad(id_actividad: int, actividad: ActividadUpdate, db: Session = Depends(get_db)):
    db_actividad = db.query(Actividad).filter(Actividad.id_actividad == id_actividad).first()
    if not db_actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")
    
    if actividad.nombre is not None:
        db_actividad.nombre = actividad.nombre
    if actividad.descripcion is not None:
        db_actividad.descripcion = actividad.descripcion
    if actividad.costo is not None:
        db_actividad.costo = actividad.costo

    db.commit()
    db.refresh(db_actividad)

    return db_actividad


#############################################################################################
#                               TURNOS                                                      #
#############################################################################################


#Trae todos los turnos disponibles
@app.get("/turnos")
async def read_turnos(db: Session = Depends(get_db)):
    turnos = db.query(Turno).all()
    if not turnos:
        raise HTTPException(status_code=404, detail="No hay turnos disponibles")
    return turnos


#Agregar turnos
@app.post("/turnos")
async def post_turno(turno: TurnoPost, db: Session = Depends(get_db)):
    nuevo_turno = Turno(hora_inicio=turno.hora_inicio, hora_fin=turno.hora_fin)
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return nuevo_turno


#Eliminar turnos
@app.delete("/turnos/{id_turno}", status_code=200)
async def delete_turno(id_turno: int, db:Session = Depends(get_db)):
    turno = db.query(Turno).filter(Turno.id_turno == id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="No se encontro un turno para eliminar")
    db.delete(turno)
    db.commit()
    return {"detail": "Turno eliminado correctamente"}


#############################################################################################
#                               ALUMNOS                                                     #
#############################################################################################

#Agregar alumnos
@app.post("/alumnos")
async def post_alumno(alumno: AlumnoPost, db: Session = Depends(get_db)):
    nuevo_alumno = Alumno(
        ci_alumno=alumno.ci_alumno,
        nombre=alumno.nombre,
        apellido=alumno.apellido,
        fecha_nacimiento=alumno.fecha_nacimiento,
        telefono=alumno.telefono,
        correo=alumno.correo
    )

    db.add(nuevo_alumno)
    db.commit()
    db.refresh(nuevo_alumno)
    return nuevo_alumno


#Eliminar alumnos
@app.delete("/alumnos/{ci_alumno}", status_code=200)
async def delete_alumno(ci_alumno: int, db: Session = Depends(get_db)):
    alumno= db.query(Alumno).filter(Alumno.ci_alumno == ci_alumno).first()
    if not alumno:
        raise HTTPException(status_code=404, detail="No se encontro el alumno")
    db.delete(alumno)
    db.commit()
    return {"detail": "Alumno eliminado correctamente"}


#Trae todos los alumnos disponibles
@app.get("/alumnos")
async def read_alumnos(db: Session = Depends(get_db)):
    alumnos = db.query(Alumno).all()
    if not alumnos:
        raise HTTPException(status_code=404, detail="No hay alumnos disponibles")
    return alumnos

    