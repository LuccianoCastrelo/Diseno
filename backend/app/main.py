#main.py
from fastapi import FastAPI, Depends, HTTPException, Body
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
#Trabajadores
@app.post("/trabajador/", response_model=schemas.TrabajadorSchema)
def create_trabajador(trabajador: schemas.TrabajadorSchema, db:Session= Depends(database.get_db)):
    db_trabajador=crud.create_trabajador(db, id_trabajador=trabajador.id_trabajador)
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
    crud.delete_trabajador(db, id_trabajador=id_trabajador)
    return db_trabajador

# Administradores
@app.post("/admin/", response_model=schemas.AdministradorSchema) 
def create_admin(admin: schemas.AdministradorSchema, db: Session = Depends(database.get_db)):
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
    if db_admin is None:
        raise HTTPException(status_code=404, detail= "Worker not found")
    crud.delete_admin(db, id_administrador=id_administrador)
    return db_admin

#crear registro de horas
@app.post("/registrohoras/", response_model=schemas.RegistroHorasTrabajadasSchema)
def create_registro(registro: schemas.RegistroHorasTrabajadasCreateSchema, db: Session = Depends(database.get_db)):
    return crud.create_registro(db=db, registro=registro)

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
    db_registro=crud.update_registro(db, id_registro=id_registro, registro_data=registro)
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
    crud.delete_registro(db, id_registro=id_registro)
    return db_registro

#crear sueldos
@app.post("/sueldos/", response_model=schemas.SueldoSchema)
def create_sueldo(sueldo: schemas.SueldoSchema, db:Session= Depends(database.get_db)):
    return crud.create_sueldo(db=db, sueldo=sueldo)

#obtener sueldo
@app.get("/sueldo/{id_sueldo}", response_model=schemas.SueldoSchema)
def read_sueldo(id_sueldo: int, db:Session=Depends(database.get_db)):
    db_sueldo=crud.get_sueldo(db, id_sueldo=id_sueldo)
    if db_sueldo is None:
        raise HTTPException(status_code=404, detail="Salary not found")
    return db_sueldo

#actualizar sueldo
@app.put("/sueldo/{id_sueldo}",response_model=schemas.SueldoSchema)
def update_sueldo(id_sueldo:int,sueldo: schemas.SueldoSchema, db:Session=Depends(database.get_db)):
    db_sueldo=crud.update_sueldo(db, id_sueldo=id_sueldo, sueldo_data=sueldo)
    if db_sueldo is None:
        raise HTTPException(status_code=404, detail="Salary not found")
    updated_sueldo=crud.update_sueldo(db, id_sueldo,sueldo)
    return updated_sueldo

#borrar sueldo
@app.delete("/sueldo/{id_sueldo}", response_model=schemas.SueldoSchema)
def delete_sueldo(id_sueldo:int, db:Session=Depends(database.get_db)):
    db_sueldo=crud.delete_sueldo(db, id_sueldo=id_sueldo)
    if db_sueldo is None:
        raise HTTPException(status_code=404, detail= "Salary not found")
    crud.delete_sueldo(db, id_sueldo=id_sueldo)
    return db_sueldo


#--------GET SUELDOS BY FECHAS-------------
@app.get("/trabajadores/{id_trabajador}/calcular_sueldo_diario")
def calcular_sueldo_diario(id_trabajador: int, fecha: str, db: Session = Depends(database.get_db)):
    resultado = crud.obtener_sueldo_diario(db, id_trabajador, fecha)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return resultado

@app.get("/trabajadores/{id_trabajador}/calcular_sueldo_semanal")
def calcular_sueldo_semanal(id_trabajador: int, fecha_inicio_semana: str, db: Session = Depends(database.get_db)):
    print(fecha_inicio_semana)
    resultado = crud.obtener_sueldo_semanal(db, id_trabajador, fecha_inicio_semana)
    if "message" in resultado:
        raise HTTPException(status_code=404, detail=resultado["message"])
    return resultado

@app.get("/trabajadores/{id_trabajador}/calcular_sueldo_mensual")
def calcular_sueldo_mensual(id_trabajador: int, mes: str, db: Session = Depends(database.get_db)):
    resultado = crud.obtener_sueldo_mensual(db, id_trabajador, mes)
    if resultado is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado")
    return resultado


#----------GET REGISTROS BY FECHAS-------------------
@app.get("/trabajadores/{trabajador_id}/registros_diarios", response_model=schemas.RegistroHorasTrabajadasListResponse)
def get_daily_logs(trabajador_id: int, fecha: str, db: Session = Depends(database.get_db)):
    try:
        registros = crud.get_daily_logs(db, trabajador_id, fecha)
        if not registros:
            return {"registros": []}
        return {"registros": registros}
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use AAAA-MM-DD.")

@app.get("/trabajadores/{trabajador_id}/registros_semanales", response_model=schemas.RegistroHorasTrabajadasListResponse)
def get_weekly_logs(trabajador_id: int, fecha_inicio_semana: str, db: Session = Depends(database.get_db)):
    try:
        registros = crud.get_weekly_logs(db, trabajador_id, fecha_inicio_semana)
        if not registros:
            return {"registros": []}
        return {"registros": registros}
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Use AAAA-MM-DD.")

@app.get("/trabajadores/{trabajador_id}/registros_mensuales", response_model=schemas.RegistroHorasTrabajadasListResponse)
def get_monthly_logs(trabajador_id: int, mes: str, db: Session = Depends(database.get_db)):
    try:
        registros = crud.get_monthly_logs(db, trabajador_id, mes)
        if not registros:
            return {"registros": []}
        return {"registros": registros}
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de mes inválido. Use MM.")

#---------------METRICS---------------------------
@app.get("/metrics/total_trabajadores")
def get_total_trabajadores(db: Session = Depends(database.get_db)):
    total_trabajadores = crud.get_total_trabajadores(db)
    return {"total_trabajadores": total_trabajadores}

@app.get("/metrics/total_horas_trabajadas")
def get_total_horas_trabajadas(db: Session = Depends(database.get_db)):
    total_horas_trabajadas = crud.get_total_horas_trabajadas(db)
    print(total_horas_trabajadas)
    return {"total_horas_trabajadas": total_horas_trabajadas}

@app.get("/metrics/total_turnos")
def get_total_turnos(db: Session = Depends(database.get_db)):
    total_turnos = crud.get_total_turnos(db)
    print(total_turnos)
    return {"total_turnos": total_turnos}

@app.get("/metrics/total_permanent_workers")
def get_total_permanent_workers(db: Session = Depends(database.get_db)):
    total_permanent_workers = crud.get_total_permanent_workers(db)
    print(total_permanent_workers)
    return {"total_permanent_workers": total_permanent_workers}

@app.get("/metrics/total_eventual_workers")
def get_total_eventual_workers(db: Session = Depends(database.get_db)):
    total_eventual_workers = crud.get_total_eventual_workers(db)
    print(total_eventual_workers)
    return {"total_eventual_workers": total_eventual_workers}
