from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Actividad, Turno, Alumno,AlumnoClase,Equipamiento,Instructor,Login,Clase, Base
from schemas import TurnoPost, ActividadPost, ActividadResponse 
from schemas import ActividadUpdate, AlumnoPost, InstructorPost, AlumnoResponse, EquipamientoPost 
from schemas import LoginRequest, LoginResponse, ClaseCreate, ClaseResponse, AlumnoClaseRequest, EquipamientoResponse, EquipamientoResponseActividad

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las direcciones
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos
    allow_headers=["*"],  # Permite todos los encabezados
)


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


#############################################################################################
#                               INSTRUCTORES                                                #
#############################################################################################

#Agrega Instructor
@app.post("/instructores")
async def post_instructor(instructor: InstructorPost, db: Session = Depends(get_db)):
    nuevo_instructor = Instructor(
        ci_instructor= instructor.ci_instructor,
        nombre=instructor.nombre,
        apellido=instructor.apellido
    )
    db.add(nuevo_instructor)
    db.commit()
    db.refresh(nuevo_instructor)
    return nuevo_instructor

#Trae todos los instructores
@app.get("/instructores")
async def read_instructores( db: Session = Depends(get_db)):
    instructores = db.query(Instructor).all()
    if not instructores:
        raise HTTPException(status_code=404, detail="No hay instructores disponibles")
    return instructores


@app.delete("/instructores/{ci_instructor}", status_code=200)
async def delete_instructor(ci_instructor: int, db: Session = Depends(get_db)):
    instructor= db.query(Instructor).filter(Instructor.ci_instructor == ci_instructor).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="No se encontro el instructor")
    db.delete(instructor)
    db.commit()
    return {"detail": "Instructor eliminado correctamente"}


#############################################################################################
#                               REGISTRO                                                    #
#############################################################################################


#Registra un alumno y guarda la cedula, correo y contraseña en la tabla login
@app.post("/register", response_model=AlumnoResponse)
async def create_alumno(alumno: AlumnoPost, db: Session = Depends(get_db)):

    db_correo = db.query(Login).filter(Login.correo == alumno.correo).first()
    if db_correo:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    db_alumno = Alumno(
        ci_alumno=alumno.ci_alumno,
        nombre=alumno.nombre,
        apellido=alumno.apellido,
        fecha_nacimiento=alumno.fecha_nacimiento,
        telefono=alumno.telefono,
        correo=alumno.correo,
        contraseña=alumno.contraseña
    )
    db.add(db_alumno)
    db.commit()
    db.refresh(db_alumno)

    db_login = Login(correo=alumno.correo, contraseña=alumno.contraseña, ci_alumno=alumno.ci_alumno)
    db.add(db_login)
    db.commit()

    return db_alumno


#############################################################################################
#                               LOGIN                                                       #
#############################################################################################

@app.post("/login", response_model=LoginResponse)  
async def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    db_usuario = db.query(Login).filter(Login.correo == login_data.correo).first()
    if not db_usuario or db_usuario.contraseña != login_data.contraseña:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    return {"message": "Inicio de sesión exitoso"}



#############################################################################################
#                               EQUIPAMIENTO                                                #
#############################################################################################

#Agregar equipamiento
@app.post("/equipamiento")
async def crear_equipamiento(equipamiento: EquipamientoPost, db: Session = Depends(get_db)):
    nuevo_equipamiento = Equipamiento(
        id_actividad=equipamiento.id_actividad,
        nombre=equipamiento.nombre,
        descripcion=equipamiento.descripcion,
        costo=equipamiento.costo
    )
    
    db.add(nuevo_equipamiento)
    db.commit()
    db.refresh(nuevo_equipamiento)

    return {"message": "Equipamiento creado correctamente.", "data": nuevo_equipamiento}

#Mostrar los equipamientos
@app.get("/equipamientos", response_model=list[EquipamientoResponse])
def get_equipamientos(db: Session = Depends(get_db)):
    equipamientos = db.query(
        Equipamiento.nombre.label("nombre_equipamiento"),
        Equipamiento.descripcion.label("descripcion_equipamiento"),
        Equipamiento.costo.label("costo_equipamiento"),
        Actividad.nombre.label("nombre_actividad")
    ).join(Actividad, Equipamiento.id_actividad == Actividad.id_actividad).all()
    
    return [{"nombre_actividad": equip.nombre_actividad,
             "nombre_equipamiento": equip.nombre_equipamiento,
             "descripcion_equipamiento": equip.descripcion_equipamiento,
             "costo_equipamiento": equip.costo_equipamiento} for equip in equipamientos]

#GET por actividad
@app.get("/equipamientos/{id_actividad}", response_model=list[EquipamientoResponseActividad])
def get_equipamientos_por_actividad(
    id_actividad: int, 
    db: Session = Depends(get_db)
):
    actividad_existente = db.query(Actividad).filter(Actividad.id_actividad == id_actividad).first()
    if not actividad_existente:
        raise HTTPException(status_code=404, detail="Actividad no encontrada.")

    equipamientos = db.query(Equipamiento).filter(Equipamiento.id_actividad == id_actividad).all()
    
    if not equipamientos:
        raise HTTPException(status_code=404, detail="No hay equipamientos para esta actividad.")
    
    return equipamientos


#############################################################################################
#                               INSCRIPCION                                                 #
#############################################################################################


#Añadir una clase
@app.post("/clase", response_model=ClaseCreate)
async def create_clase(clase: ClaseCreate, db: Session = Depends(get_db)):

    instructor = db.query(Instructor).filter(Instructor.ci_instructor == clase.ci_instructor).first()
    if not instructor:
        raise HTTPException(status_code=404, detail="Instructor no encontrado")

    actividad = db.query(Actividad).filter(Actividad.id_actividad == clase.id_actividad).first()
    if not actividad:
        raise HTTPException(status_code=404, detail="Actividad no encontrada")

    turno = db.query(Turno).filter(Turno.id_turno == clase.id_turno).first()
    if not turno:
        raise HTTPException(status_code=404, detail="Turno no encontrado")

    nueva_clase = Clase(
        ci_instructor=clase.ci_instructor,
        id_actividad=clase.id_actividad,
        id_turno=clase.id_turno,
        dictada=clase.dictada
    )

    db.add(nueva_clase)
    db.commit()
    db.refresh(nueva_clase)

    return nueva_clase

#Mostrar clases
@app.get("/clases", response_model=list[ClaseResponse])
def get_clases(db: Session = Depends(get_db)):
    # Realiza la consulta con los joins necesarios
    clases = db.query(
        Clase.id_clase,
        Actividad.nombre.label("nombre_actividad"),
        Actividad.costo.label("costo_actividad"),
        Instructor.nombre.label("nombre_instructor"),
        Turno.hora_inicio.label("hora_inicio"),
        Turno.hora_fin.label("hora_fin")
    ).join(Actividad, Clase.id_actividad == Actividad.id_actividad
    ).join(Instructor, Clase.ci_instructor == Instructor.ci_instructor
    ).join(Turno, Clase.id_turno == Turno.id_turno
    ).all()
    
    # Devuelve el resultado en el formato adecuado
    return [{"id_clase": clase.id_clase,"costo_actividad":clase.costo_actividad, "nombre_actividad": clase.nombre_actividad, 
             "nombre_instructor": clase.nombre_instructor, 
             "hora_inicio":clase.hora_inicio, "hora_fin":clase.hora_fin} for clase in clases]



#Poder inscribirse a una clase
@app.post("/inscribir_alumno")
async def inscribir_alumno(alumno_clase: AlumnoClaseRequest, db: Session = Depends(get_db)):
    # Verificar si el alumno ya está inscrito en la clase
    existe = db.query(AlumnoClase).filter_by(id_clase=alumno_clase.id_clase, ci_alumno=alumno_clase.ci_alumno).first()
    
    if existe:
        raise HTTPException(status_code=400, detail="El alumno ya está inscrito en esta clase.")

    # Crear un nuevo registro de inscripción
    nueva_inscripcion = AlumnoClase(
        id_clase=alumno_clase.id_clase,
        ci_alumno=alumno_clase.ci_alumno,
        id_equipamiento=alumno_clase.id_equipamiento
    )
    
    db.add(nueva_inscripcion)
    db.commit()
    db.refresh(nueva_inscripcion)

    return {"message": "Alumno inscrito correctamente.", "data": nueva_inscripcion}
