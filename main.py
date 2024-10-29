from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Actividad, Base

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/actividades")
async def read_actividades(db: Session = Depends(get_db)):
    actividades = db.query(Actividad).all()
    if not actividades:
        raise HTTPException(status_code=404, detail="No hay actividades")
    return actividades