#crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_trabajador(db: Session, trabajador: schemas.TrabajadorSchema):
    db_trabajador = models.Trabajador(nombre=trabajador.nombre)
    db.add(db_trabajador)
    db.commit()
    db.refresh(db_trabajador)
    return db_trabajador

def get_trabajador(db: Session, id_trabajador: int):
    """
    Fetch a Trabajador (worker) by id_trabajador from the database.
    
    Parameters:
    db (Session): The SQLAlchemy session for querying the database.
    id_trabajador (int): The ID of the worker to fetch.
    
    Returns:
    Trabajador: The Trabajador instance if found, otherwise None.
    """
    return db.query(models.Trabajador).filter(models.Trabajador.id_trabajador == id_trabajador).first()


def get_all_trabajadores(db: Session):
    return db.query(models.Trabajador).all()

def update_trabajador(db: Session, id_trabajador: int, trabajador_data: schemas.TrabajadorSchema):
    db_trabajador = db.query(models.Trabajador).filter(models.Trabajador.id_trabajador == id_trabajador).first()
    if db_trabajador:
        db_trabajador.nombre = trabajador_data.nombre
        db.commit()
        db.refresh(db_trabajador)
        return db_trabajador
    return None

def delete_trabajador(db: Session, id_trabajador: int):
    db_trabajador = db.query(models.Trabajador).filter(models.Trabajador.id_trabajador == id_trabajador).first()
    if db_trabajador:
        db.delete(db_trabajador)
        db.commit()
        return db_trabajador
    return None

def get_admin(db: Session, id_administrador: int):
    return db.query(models.Administrador).filter(models.Administrador.id_administrador == id_administrador).first()

def create_admin(db: Session, admin: schemas.AdministradorSchema):
    db_admin = models.Administrador(nombre=admin.nombre, correo=admin.correo)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_admin(db: Session, id_administrador: int, admin_data: schemas.AdministradorSchema):
    db_admin = db.query(models.Administrador).filter(models.Administrador.id_administrador == id_administrador).first()
    if db_admin:
        db_admin.nombre = admin_data.nombre
        db_admin.correo = admin_data.correo
        db.commit()
        db.refresh(db_admin)
        return db_admin
    return None

def delete_admin(db: Session, id_administrador: int):
    db_admin = db.query(models.Administrador).filter(models.Administrador.id_administrador == id_administrador).first()
    if db_admin:
        db.delete(db_admin)
        db.commit()
        return db_admin
    return None

def get_turno(db: Session, id_turno: int):
    return db.query(models.Turno).filter(models.Turno.id_turno == id_turno).first()

def create_turno(db: Session, turno: schemas.TurnoSchema):
    db_turno = models.Turno(
        id_trabajador=turno.id_trabajador,
        hora_inicio=turno.hora_inicio,
        hora_fin=turno.hora_fin,
        duracion=turno.duracion
    )
    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)
    return db_turno

def update_turno(db: Session, id_turno: int, turno_data: schemas.TurnoSchema):
    db_turno = db.query(models.Turno).filter(models.Turno.id_turno == id_turno).first()
    if db_turno:
        db_turno.hora_inicio = turno_data.hora_inicio
        db_turno.hora_fin = turno_data.hora_fin
        db_turno.duracion = turno_data.duracion
        db.commit()
        db.refresh(db_turno)
        return db_turno
    return None

def delete_turno(db: Session, id_turno: int):
    db_turno = db.query(models.Turno).filter(models.Turno.id_turno == id_turno).first()
    if db_turno:
        db.delete(db_turno)
        db.commit()
        return db_turno
    return None

# --------- CRUD para Registro de Horas Trabajadas ---------
def get_registro(db: Session, id_registro: int):
    return db.query(models.RegistroHorasTrabajadas).filter(models.RegistroHorasTrabajadas.id_registro == id_registro).first()

def create_registro(db: Session, registro: schemas.RegistroHorasTrabajadasSchema):
    db_registro = models.RegistroHorasTrabajadas(
        id_trabajador=registro.id_trabajador,
        id_turno=registro.id_turno,
        fecha=registro.fecha,
        horas_trabajadas=registro.horas_trabajadas
    )
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro

def update_registro(db: Session, id_registro: int, registro_data: schemas.RegistroHorasTrabajadasSchema):
    db_registro = db.query(models.RegistroHorasTrabajadas).filter(models.RegistroHorasTrabajadas.id_registro == id_registro).first()
    if db_registro:
        db_registro.id_trabajador = registro_data.id_trabajador
        db_registro.id_turno = registro_data.id_turno
        db_registro.fecha = registro_data.fecha
        db_registro.horas_trabajadas = registro_data.horas_trabajadas
        db.commit()
        db.refresh(db_registro)
        return db_registro
    return None

def delete_registro(db: Session, id_registro: int):
    db_registro = db.query(models.RegistroHorasTrabajadas).filter(models.RegistroHorasTrabajadas.id_registro == id_registro).first()
    if db_registro:
        db.delete(db_registro)
        db.commit()
        return db_registro
    return None