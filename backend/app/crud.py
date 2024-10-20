#crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from .algorithm import *
from datetime import datetime

# --------- CRUD para Trabajadores ---------
def get_trabajador(db: Session, id_trabajador: int):
    return db.query(models.Trabajador).filter(models.Trabajador.id_trabajador == id_trabajador).first()

def get_all_trabajadores(db: Session):
    return db.query(models.Trabajador).all()

def create_trabajador(db: Session, trabajador: schemas.TrabajadorSchemaReq):
    db_trabajador = models.Trabajador(
        nombre=trabajador.nombre,
        tipo=trabajador.tipo,
        pago_por_turno=trabajador.pago_por_turno,
        salario_base=trabajador.salario_base,
        rut=trabajador.rut  # Incluir el rut en la creación
    )
    db.add(db_trabajador)
    db.commit()
    db.refresh(db_trabajador)
    return db_trabajador


def update_trabajador(db: Session, id_trabajador: int, trabajador_data: schemas.TrabajadorSchema):
    db_trabajador = get_trabajador(db, id_trabajador)
    if db_trabajador:
        db_trabajador.nombre = trabajador_data.nombre
        db.commit()
        db.refresh(db_trabajador)
        return db_trabajador
    return None

def delete_trabajador(db: Session, id_trabajador: int):
    db_trabajador = get_trabajador(db, id_trabajador)
    if db_trabajador:
        db.delete(db_trabajador)
        db.commit()
        return db_trabajador
    return None

def get_trabajador_by_rut(db: Session, rut: str):
    return db.query(models.Trabajador).filter(models.Trabajador.rut == rut).first()

# --------- CRUD para Administradores ---------
def get_admin(db: Session, id_administrador: int):
    return db.query(models.Administrador).filter(models.Administrador.id_administrador == id_administrador).first()

def create_admin(db: Session, admin: schemas.AdministradorSchema):
    db_admin = models.Administrador(nombre=admin.nombre, correo=admin.correo)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

def update_admin(db: Session, id_administrador: int, admin_data: schemas.AdministradorSchema):
    db_admin = get_admin(db, id_administrador)
    if db_admin:
        db_admin.nombre = admin_data.nombre
        db_admin.correo = admin_data.correo
        db.commit()
        db.refresh(db_admin)
        return db_admin
    return None


def delete_admin(db: Session, id_administrador: int):
    db_admin = get_admin(db, id_administrador)
    if db_admin:
        db.delete(db_admin)
        db.commit()
        return db_admin
    return None

# --------- CRUD para Registro de Horas Trabajadas ---------
def get_registro(db: Session, id_registro: int):
    return db.query(models.RegistroHorasTrabajadas).filter(models.RegistroHorasTrabajadas.id_registro == id_registro).first()



def create_registro(db: Session, registro: schemas.RegistroHorasTrabajadasCreateSchema):
    # Calcular las horas trabajadas
    formato_hora = "%H:%M:%S"
    hora_inicio_dt = datetime.strptime(str(registro.hora_inicio), formato_hora)
    hora_fin_dt = datetime.strptime(str(registro.hora_fin), formato_hora)
    delta_horas = (hora_fin_dt - hora_inicio_dt).seconds / 3600  # Convertimos a horas

    # Determinar si la fecha es domingo
    es_domingo = registro.fecha.weekday() == 6  # Si el día de la semana es 6, es domingo

    # Calcular turnos basados en las horas trabajadas
    turnos = calcular_turnos(delta_horas)

    # Crear el registro en la base de datos
    db_registro = models.RegistroHorasTrabajadas(
        id_trabajador=registro.id_trabajador,
        fecha=registro.fecha,
        hora_inicio=registro.hora_inicio,
        hora_fin=registro.hora_fin,
        horas_trabajadas=delta_horas,
        es_domingo=es_domingo,  # Guardamos si es domingo o no
        cantidad_turnos_trabajados=turnos
    )
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro


def update_registro(db: Session, id_registro: int, registro_data: schemas.RegistroHorasTrabajadasSchema):
    db_registro = get_registro(db, id_registro)
    if db_registro:
        db_registro.id_trabajador = registro_data.id_trabajador
        db_registro.id_turno = registro_data.id_turno
        db_registro.fecha = registro_data.fecha
        db_registro.horas_trabajadas = registro_data.horas_trabajadas
        db_registro.cantidad_turnos_trabajados = registro_data.cantidad_turnos_trabajados
        db.commit()
        db.refresh(db_registro)
        return db_registro
    return None

def delete_registro(db: Session, id_registro: int):
    db_registro = get_registro(db, id_registro)
    if db_registro:
        db.delete(db_registro)
        db.commit()
        return db_registro
    return None

def create_sueldo(db: Session, sueldo: schemas.SueldoSchema):
    db_sueldo = models.Sueldo(id_trabajador=sueldo.id_trabajador, fecha=sueldo.fecha)
    db.add(db_sueldo)
    db.commit()
    db.refresh(db_sueldo)
    return db_sueldo

# Obtener un sueldo por su ID
def get_sueldo(db: Session, id_sueldo: int):
    return db.query(models.Sueldo).filter(models.Sueldo.id_sueldo == id_sueldo).first()

# Obtener todos los sueldos de un trabajador
def get_sueldos_by_trabajador(db: Session, id_trabajador: int):
    return db.query(models.Sueldo).filter(models.Sueldo.id_trabajador == id_trabajador).all()

# Actualizar un sueldo existente
def update_sueldo(db: Session, id_sueldo: int, sueldo_data: schemas.SueldoSchema):
    db_sueldo = get_sueldo(db, id_sueldo=id_sueldo)
    if db_sueldo:
        db_sueldo.fecha = sueldo_data.fecha
        db.commit()
        db.refresh(db_sueldo)
        return db_sueldo
    return None

# Eliminar un sueldo por su ID
def delete_sueldo(db: Session, id_sueldo: int):
    db_sueldo = get_sueldo(db, id_sueldo=id_sueldo)
    if db_sueldo:
        db.delete(db_sueldo)
        db.commit()
        return db_sueldo
    return None

# --------- Métodos adicionales ---------
def get_registros_horas(db: Session, id_trabajador: int):
    return db.query(models.RegistroHorasTrabajadas).filter(models.RegistroHorasTrabajadas.id_trabajador == id_trabajador).all()

# Función para crear un ID aleatorio
def generate_random_id(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))