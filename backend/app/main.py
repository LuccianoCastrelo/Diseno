#main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, database
from fastapi.middleware.cors import CORSMiddleware
models.Base.metadata.create_all(bind=database.engine)
app = FastAPI()

# Orígenes permitidos (puedes agregar más si los necesitas)
origins = ["http://localhost:5173", "http://127.0.0.1:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permite solicitudes desde estos orígenes
    allow_credentials=False,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, etc.)
    allow_headers=["*"],   # Permite todos los encabezados
)
"""
# Trabajadores
@app.post("/trabajador/", response_model=schemas.TrabajadorSchema)
def create_trabajador(trabajador: schemas.TrabajadorSchema, db:Session= Depends(database.get_db)):
    db_trabajador=crud.create_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador:
        raise HTTPException(status_code=400, detail="ID already registered")
    return crud.create_trabajador(db=db, trabajador=trabajador)
"""

@app.post("/trabajadores/", response_model=schemas.TrabajadorSchema)
def create_trabajador(trabajador: schemas.TrabajadorSchemaReq, db: Session = Depends(database.get_db)):
    # Verificar si un trabajador con el mismo rut ya existe
    db_trabajador = crud.get_trabajador_by_rut(db, rut=trabajador.rut)
    if db_trabajador:
        raise HTTPException(status_code=400, detail="El trabajador con este RUT ya está registrado")
    
    # Crear el nuevo trabajador si no existe uno con el mismo rut
    nuevo_trabajador = crud.create_trabajador(db=db, trabajador=trabajador)
    return nuevo_trabajador


@app.get("/trabajador/{id_trabajador}", response_model=schemas.TrabajadorSchema)
def read_trabajador(id_trabajador: int, db: Session = Depends(database.get_db)):
    db_trabajador = crud.get_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return db_trabajador

@app.put("/trabajador/{id_trabajador}", response_model=schemas.TrabajadorSchema)
def update_trabajador(id_trabajador: int, trabajador: schemas.TrabajadorSchema, db: Session = Depends(database.get_db)):
    db_trabajador = crud.get_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    return crud.update_trabajador(db, id_trabajador, trabajador)

@app.get("/trabajadores/", response_model=List[schemas.TrabajadorSchema])
def read_trabajadores(db: Session = Depends(database.get_db)):
    return crud.get_all_trabajadores(db)

@app.delete("/trabajador/{id_trabajador}", response_model=schemas.TrabajadorSchema)
def delete_trabajador(id_trabajador: int, db: Session = Depends(database.get_db)):
    db_trabajador = crud.get_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    crud.delete_trabajador(db, id_trabajador)
    return db_trabajador
# Administradores
@app.post("/admin/", response_model=schemas.AdministradorSchema) 
def create_admin(admin: schemas.AdministradorSchema, db: Session = Depends(database.get_db)):
    db_admin = crud.get_admin_by_id(db, id_administrador=admin.id_administrador)
    if db_admin:
        raise HTTPException(status_code=400, detail="ID already registered")
    return crud.create_admin(db=db, admin=admin)

@app.get("/admin/{id_administrador}", response_model=schemas.AdministradorSchema)
def read_admin(id_administrador: int, db: Session = Depends(database.get_db)):
    db_admin = crud.get_admin(db, id_administrador=id_administrador)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return db_admin

@app.put("/admin/{id_administrador}", response_model=schemas.AdministradorSchema)
def update_admin(id_administrador: int, admin: schemas.AdministradorSchema, db: Session = Depends(database.get_db)):
    db_admin = crud.get_admin(db, id_administrador=id_administrador)
    if db_admin is None:
        raise HTTPException(status_code=404, detail="Admin not found")
    return crud.update_admin(db, id_administrador, admin)

@app.delete("/admin/{id_administrador}", response_model=schemas.AdministradorSchema)
def delete_admin(id_administrador:int,admin: schemas.AdministradorSchema, db:Session=Depends(database.get_db)):
    db_admin=crud.delete_admin(db, id_administrador=id_administrador)
    if admin is None:
        raise HTTPException(status_code=404, detail= "Worker not found")
    crud.delete_admin(db,admin,)
    return db_admin

#crear turno
@app.post("/turno/", response_model=schemas.TurnoSchema)
def create_turno(turno: schemas.TurnoSchema, db:Session= Depends(database.get_db)):
    db_turno=crud.create_turno(db, id_turno=id_turno)
    if db_turno:
        raise HTTPException(status_code=400, detail="ID already registered")
    db_turno=crud.create_turno(db=db, turno=turno)
    return db_turno

#obtener turno
@app.get("/turno/{id_turno}", response_model=schemas.TurnoSchema)
def read_turno(id_turno: int, db:Session=Depends(database.get_db)):
    db_turno=crud.get_turno(db, id_turno=id_turno)
    if db_turno is None:
        raise HTTPException(status_code=404, detail="turno not found")
    return db_turno

#actualizar turno
@app.put("/turno/{id_turno}",response_model=schemas.TurnoSchema)
def update_turno(id_turno:int,turno: schemas.TurnoSchema, db:Session=Depends(database.get_db)):
    db_turno=crud.update_turno(db, id_turno=id_turno)
    if db_turno is None:
        raise HTTPException(status_code=404, detail="turno not found")
    updated_turno=crud.update_turno(db, id_turno,turno)
    return updated_turno

#borrar turno
@app.delete("/turno/{id_turno}", response_model=schemas.TurnoSchema)
def delete_turno(id_turno:int,turno: schemas.TurnoSchema, db:Session=Depends(database.get_db)):
    db_turno=crud.delete_turno(db, id_turno=id_turno)
    if turno is None:
        raise HTTPException(status_code=404, detail= "Turno not found")
    crud.delete_turno(db,turno,)
    return db_turno

#crear registro de horas
@app.post("/registrohoras/", response_model=schemas.RegistroHorasTrabajadasSchema)
def create_registro(registro: schemas.RegistroHorasTrabajadasSchema, db:Session= Depends(database.get_db)):
    db_registro=crud.create_registro(db, id_registro=id_registro)
    if db_registro:
        raise HTTPException(status_code=400, detail="Time log already registered")
    db_registro=crud.create_registro(db=db, registro=registro)
    return db_registro
 
#obtener registro de horas
@app.get("/registro/{id_registro}", response_model=schemas.RegistroHorasTrabajadasSchema)
def read_registro(id_registro: int, db:Session=Depends(database.get_db)):
    db_registro=crud.get_registro(db, id_registro=id_registro)
    if db_registro is None:
        raise HTTPException(status_code=404, detail="Time log not found")
    return db_registro

#actualizar registro de horas

@app.put("/registro/{id_registro}",response_model=schemas.RegistroHorasTrabajadasSchema)
def update_registro(id_registro:int,registro: schemas.RegistroHorasTrabajadasSchema, db:Session=Depends(database.get_db)):
    db_registro=crud.update_registro(db, id_registro=id_registro)
    if db_registro is None:
        raise HTTPException(status_code=404, detail="Time log not found")
    updated_registro=crud.update_registro(db, id_registro,registro)
    return updated_registro

#borrar registro de horas
@app.delete("/registro/{id_registro}", response_model=schemas.RegistroHorasTrabajadasSchema)
def delete_registro(id_registro:int,registro: schemas.RegistroHorasTrabajadasSchema, db:Session=Depends(database.get_db)):
    db_registro=crud.delete_registro(db, id_registro=id_registro)
    if registro is None:
        raise HTTPException(status_code=404, detail= "Time log not found")
    crud.delete_registro(db,registro,)
    return db_registro

# Calcular pagos
@app.post("/calcular_pagos/{id_trabajador}", response_model=schemas.TrabajadorSchema)
def calcular_pagos(id_trabajador: int, db: Session = Depends(database.get_db)):
    db_trabajador = crud.get_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    
    registros_horas = crud.get_registros_horas(db, id_trabajador=id_trabajador)
    if not registros_horas:
        raise HTTPException(status_code=404, detail="No hay registros de horas trabajadas para este trabajador.")
    
    trabajador_data = {
        "nombre": db_trabajador.nombre,
        "tipo": db_trabajador.tipo,
        "pago_por_turno": db_trabajador.pago_por_turno,
        "salario_base": db_trabajador.salario_base
    }
    
    registros_jornadas = [
        {"fecha": registro.fecha.strftime('%d-%m-%Y'), "horas_trabajadas": registro.horas_trabajadas, "es_festivo_o_domingo": False}
        for registro in registros_horas
    ]
    
    resultado = calcular_pago_trabajador(trabajador_data, registros_jornadas)
    
    return {
        "nombre": db_trabajador.nombre,
        "pago_total": resultado["pago_total"],
        "pagos_semanales": resultado["pagos_semanales"],
        "pagos_mensuales": resultado["pagos_mensuales"]
    }