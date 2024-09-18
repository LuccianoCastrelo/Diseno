from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

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

@app.delete("/trabajador/{id_trabajador}", response_model=schemas.TrabajadorSchema)
def delete_trabajador(id_trabajador:int,trabajador: schemas.TrabajadorSchema, db:Session=Depends(database.get_db)):
    db_trabajador=crud.get_trabajador(db, id_trabajador=id_trabajador)
    if db_trabajador is None:
        raise HTTPException(status_code=404, detail= "Worker not found")
    crud.delete_trabajador(db,trabajador,)
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