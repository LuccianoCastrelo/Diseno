from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, database
from datetime import datetime
from .algorithm import *
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow your frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(database.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/trabajador/", response_model=schemas.TrabajadorSchema)
def create_trabajador(trabajador: schemas.TrabajadorSchema, db:Session= Depends(database.get_db)):
    db_trabajador=crud.get_trabajador_by_id(db, id_trabajador=id_trabajador)
    if db_trabajador:
        raise HTTPException(status_code=400, detail="ID already registered")
    db_trabajador=crud.create_trabajador(db=db, trabajador=trabajador)
    return db_trabajador

@app.get("/trabajador/{id_trabajador}", response_model=schemas.TrabajadorSchema)
def read_trabajador(id_trabajador: int, db:Session=Depends(database.get_db)):
    db_trabajador=crud.get_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_trabajador

@app.put("/trabajador/{id_trabajador}",response_model=schemas.TrabajadorSchema)
def update_trabajador(id_trabajador:int,trabajador: schemas.TrabajadorSchema, db:Session=Depends(database.get_db)):
    db_trabajador=crud.get_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    updated_trabajador=crud.update_trabajador(db, id_trabajador,trabajador)
    return updated_trabajador

@app.get("/trabajadores/", response_model=List[schemas.TrabajadorSchema])
def read_trabajadores(db: Session = Depends(database.get_db)):
    trabajadores = crud.get_all_trabajadores(db)
    return trabajadores

@app.delete("/trabajador/{id_trabajador}", response_model=schemas.TrabajadorSchema)
def delete_trabajador(id_trabajador: int, db: Session = Depends(database.get_db)):
    db_trabajador = crud.get_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    crud.delete_trabajador(db, id_trabajador)
    return db_trabajador

@app.post("/admin/", response_model=schemas.AdministradorSchema)
def create_admin(admin: schemas.AdministradorSchema, db:Session= Depends(database.get_db)):
    db_admin=crud.get_admin_by_id(db, id_administrador=id_administrador)
    if db_admin:
        raise HTTPException(status_code=400, detail="ID already registered")
    db_admin=crud.create_admin(db=db, admin=admin)
    return db_admin

@app.get("/admin/{id_administrador}", response_model=schemas.AdministradorSchema)
def read_admin(id_administrador: int, db:Session=Depends(database.get_db)):
    db_admin=crud.get_admin(db, id_administrador=id_administrador)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_admin

@app.put("/admin/{id_administrador}",response_model=schemas.AdministradorSchema)
def update_admin(id_administrador:int,admin: schemas.AdministradorSchema, db:Session=Depends(database.get_db)):
    db_admin=crud.get_admin(db, id_administrador=id_administrador)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    updated_admin=crud.update_admin(db, id_administrador,admin)
    return updated_admin

@app.delete("/admin/{id_administrador}", response_model=schemas.AdministradorSchema)
def delete_admin(id_administrador:int,admin: schemas.AdministradorSchema, db:Session=Depends(database.get_db)):
    db_admin=crud.get_admin(db, id_administrador=id_administrador)
    if admin is None:
        raise HTTPException(status_code=404, detail= "Worker not found")
    crud.delete_admin(db,admin,)
    return db_admin

@app.post("/calcular_pagos/{id_trabajador}", response_model=schemas.TrabajadorSchema)
def calcular_pagos(id_trabajador: int, db: Session = Depends(database.get_db)):
    # Obtener el trabajador desde la base de datos
    db_trabajador = crud.get_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    
    # Obtener los registros de horas trabajadas del trabajador
    registros_horas = crud.get_registros_horas(db, id_trabajador=id_trabajador)
    
    if not registros_horas:
        raise HTTPException(status_code=404, detail="No hay registros de horas trabajadas para este trabajador.")
    
    # Preparar la información del trabajador y registros en el formato esperado por el algoritmo
    trabajador_data = {
        "nombre": db_trabajador.nombre,
        "tipo": db_trabajador.tipo,  # Extraído desde la tabla Trabajador
        "pago_por_turno": db_trabajador.pago_por_turno,  # Extraído desde la tabla Trabajador
        "salario_base": db_trabajador.salario_base  # Solo para trabajadores permanentes
    }
    
    registros_jornadas = []
    for registro in registros_horas:
        registros_jornadas.append({
            "fecha": registro.fecha.strftime('%d-%m-%Y'),
            "horas_trabajadas": registro.horas_trabajadas,
            "es_festivo_o_domingo": False  # Puedes agregar lógica para determinar si es festivo o domingo
        })
    
    # Calcular pagos usando el algoritmo
    resultado = calcular_pago_trabajador(trabajador_data, registros_jornadas)
    
    return {
        "nombre": db_trabajador.nombre,
        "pago_total": resultado["pago_total"],
        "pagos_semanales": resultado["pagos_semanales"],
        "pagos_mensuales": resultado["pagos_mensuales"]
    }
