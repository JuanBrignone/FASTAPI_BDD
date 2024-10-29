from pydantic import BaseModel
from datetime import time

class TurnoPost(BaseModel):
    hora_inicio: time
    hora_fin: time