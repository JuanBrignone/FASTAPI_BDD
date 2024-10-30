from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Actividad, Turno, Base
from schemas import TurnoPost

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#Trae todas las actividades
@app.get("/actividades")
async def read_actividades(db: Session = Depends(get_db)):
    actividades = db.query(Actividad).all()
    if not actividades:
        raise HTTPException(status_code=404, detail="No hay actividades disponibles")
    return actividades


#Trae todos los turnos disponibles
@app.get("/turnos")
async def read_turnos(db: Session = Depends(get_db)):
    turnos = db.query(Turno).all()
    if not turnos:
        raise HTTPException(status_code=404, detail="No hay turnos disponibles")
    return turnos


#Añadir más turnos
@app.post("/turnos")
async def post_turno(turno: TurnoPost, db: Session = Depends(get_db)):
    db_turno = Turno(hora_inicio=turno.hora_inicio, hora_fin=turno.hora_fin)
    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)
    return db_turno


#Eliminar turnos
@app.delete("/turnos/{id_turno}", status_code=204)
async def delete_turno(id_turno: int, db:Session = Depends(get_db)):
    turno = db.query(Turno).filter(Turno.id_turno == id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="No se encontro un turno para eliminar")
    db.delete(turno)
    db.commit()
    return {"detail": "Turno eliminado correctamente"}