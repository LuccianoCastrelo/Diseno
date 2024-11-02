#crud.py
from sqlalchemy.orm import Session
from . import models, schemas
from .algorithm import *
from datetime import datetime,timedelta
import random
from typing import List
from .models import *
from sqlalchemy import extract,func,Date,cast

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

#----------------GET SUELDOS BY FECHAS-----------------
def obtener_sueldo_mensual(db: Session, id_trabajador: int, mes: str):
    trabajador = db.query(Trabajador).filter(Trabajador.id_trabajador == id_trabajador).first()
    if not trabajador:
        return None

    # Filtrar registros de jornada por trabajador y mes especificado
    registros_jornadas = db.query(RegistroHorasTrabajadas).filter(
        RegistroHorasTrabajadas.id_trabajador == id_trabajador,
        extract('month', RegistroHorasTrabajadas.fecha) == int(mes)
    ).all()

    total_turnos, sueldo_mensual = calcular_sueldo_mensual(trabajador, registros_jornadas)
    return {"total_turnos": total_turnos, "sueldo_mensual": sueldo_mensual}

def obtener_sueldo_diario(db: Session, id_trabajador: int, fecha: str):
    trabajador = db.query(Trabajador).filter(Trabajador.id_trabajador == id_trabajador).first()
    if not trabajador:
        return None

    registros_jornada = db.query(RegistroHorasTrabajadas).filter(
        RegistroHorasTrabajadas.id_trabajador == id_trabajador,
        RegistroHorasTrabajadas.fecha == fecha
    ).all()

    _, sueldo_diario = calcular_pago_por_jornada(trabajador, registros_jornada[0].horas_trabajadas, registros_jornada[0].es_domingo)
    return {"sueldo_diario": sueldo_diario}

def obtener_sueldo_semanal(db: Session, id_trabajador: int, fecha_inicio_semana: str):
    trabajador = db.query(Trabajador).filter(Trabajador.id_trabajador == id_trabajador).first()
    if not trabajador:
        return {"message": "Trabajador no encontrado"}
    
    # Convertir la fecha proporcionada a un objeto datetime
    fecha_inicio = datetime.strptime(fecha_inicio_semana, "%Y-%m-%d")
    # Asegurar que fecha_inicio sea el lunes de esa semana
    inicio_semana = fecha_inicio - timedelta(days=fecha_inicio.weekday())  # Ajustar al lunes de la semana
    
    # Generar todas las fechas de la semana (de lunes a domingo)
    dias_semana = [inicio_semana + timedelta(days=i) for i in range(7)]
    print("Inicio de la semana (lunes):", inicio_semana)
    print("Días calculados para la semana:", [dia.strftime("%Y-%m-%d") for dia in dias_semana])
    
    # Obtener los registros de horas trabajadas de cada día de la semana
    registros_semanales = db.query(RegistroHorasTrabajadas).filter(
        RegistroHorasTrabajadas.id_trabajador == id_trabajador,
        RegistroHorasTrabajadas.fecha.in_([dia.date() for dia in dias_semana])
    ).all()
    
    # Si no hay registros, devolver un mensaje
    if not registros_semanales:
        return {"message": "No hay registros en la semana seleccionada."}

    # Convertir los registros de la semana en un formato compatible con calcular_sueldo_semanal
    registros_jornadas_semanales = [
        {
            "horas_trabajadas": registro.horas_trabajadas,
            "es_festivo_o_domingo": registro.es_domingo
        }
        for registro in registros_semanales
    ]
    
    # Calcular el sueldo semanal utilizando calcular_sueldo_semanal
    total_turnos, sueldo_semanal = calcular_sueldo_semanal(trabajador, registros_jornadas_semanales)
    
    return {"sueldo_semanal": sueldo_semanal}

#--------------------GET REGISTROS BY FECHA---------------------
def get_daily_logs(db: Session, trabajador_id: int, fecha: str) -> list[RegistroHorasTrabajadas]:
    fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    registros = db.query(RegistroHorasTrabajadas).filter(
        RegistroHorasTrabajadas.id_trabajador == trabajador_id,
        RegistroHorasTrabajadas.fecha == fecha_obj  # Sin `cast`, compara directamente
    ).all()
    print(f"Fecha buscada: {fecha_obj}")
    print("Registros encontrados:", registros)
    return registros


def get_weekly_logs(db: Session, trabajador_id: int, fecha_inicio_semana: str) -> list[RegistroHorasTrabajadas]:
    fecha_obj = datetime.strptime(fecha_inicio_semana, "%Y-%m-%d")
    fecha_fin_semana = fecha_obj + timedelta(days=6)
    registros = db.query(RegistroHorasTrabajadas).filter(
        RegistroHorasTrabajadas.id_trabajador == trabajador_id,
        RegistroHorasTrabajadas.fecha >= fecha_obj,
        RegistroHorasTrabajadas.fecha <= fecha_fin_semana
    ).all()
    return registros

def get_monthly_logs(db: Session, trabajador_id: int, mes: str) -> list[RegistroHorasTrabajadas]:
    fecha_inicio_mes = datetime.strptime(mes, "%m").replace(year=datetime.now().year, day=1)
    fecha_fin_mes = (fecha_inicio_mes.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    registros = db.query(RegistroHorasTrabajadas).filter(
        RegistroHorasTrabajadas.id_trabajador == trabajador_id,
        RegistroHorasTrabajadas.fecha >= fecha_inicio_mes,
        RegistroHorasTrabajadas.fecha <= fecha_fin_mes
    ).all()
    return registros

def get_total_trabajadores(db: Session):
    return db.query(models.Trabajador).count()

def get_total_horas_trabajadas(db: Session):
    return db.query(func.sum(models.RegistroHorasTrabajadas.horas_trabajadas)).scalar()

def get_total_turnos(db: Session):
    return db.query(func.sum(models.RegistroHorasTrabajadas.cantidad_turnos_trabajados)).scalar()

def get_total_permanent_workers(db: Session):
    return db.query(models.Trabajador).filter(models.Trabajador.tipo == "permanente").count()

def get_total_eventual_workers(db: Session):
    return db.query(models.Trabajador).filter(models.Trabajador.tipo == "eventual").count()
