from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


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

def get_trabajador(db: Session, id_trabajador: int):
    """
    Obtener el trabajador y su información adicional, como tipo, pago por turno y salario base.
    """
    return db.query(models.Trabajador).filter(models.Trabajador.id_trabajador == id_trabajador).first()

def get_registros_horas(db: Session, id_trabajador: int):
    """
    Obtener los registros de horas trabajadas de un trabajador específico.
    """
    return db.query(models.RegistroHorasTrabajadas).filter(models.RegistroHorasTrabajadas.id_trabajador == id_trabajador).all()
