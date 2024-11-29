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
    """
    Crea un nuevo registro de horas trabajadas en la base de datos.
    """
    # Calcular las horas trabajadas
    formato_hora = "%H:%M:%S"
    hora_inicio_dt = datetime.strptime(str(registro.hora_inicio), formato_hora)
    hora_fin_dt = datetime.strptime(str(registro.hora_fin), formato_hora)
    delta_horas = (hora_fin_dt - hora_inicio_dt).seconds / 3600  # Convertimos a horas

    # Determinar si la fecha es domingo
    es_domingo = registro.fecha.weekday() == 6

    # Calcular turnos basados en las horas trabajadas
    turnos = calcular_turnos(delta_horas)

    # Crear el registro en la base de datos
    db_registro = models.RegistroHorasTrabajadas(
        id_trabajador=registro.id_trabajador,
        fecha=registro.fecha,
        hora_inicio=registro.hora_inicio,
        hora_fin=registro.hora_fin,
        horas_trabajadas=delta_horas,
        cantidad_turnos_trabajados=turnos,
        es_domingo=es_domingo,
        id_maquina=registro.id_maquina,  # Asociar la máquina si se proporciona
        id_cliente=registro.id_cliente   # Asociar el cliente
    )
    db.add(db_registro)
    db.commit()
    db.refresh(db_registro)
    return db_registro

def update_registro(db: Session, id_registro: int, registro_data: schemas.RegistroHorasTrabajadasSchema):
    db_registro = get_registro(db, id_registro)
    if db_registro:
        db_registro.id_trabajador = registro_data.id_trabajador
        db_registro.fecha = registro_data.fecha
        db_registro.hora_inicio = registro_data.hora_inicio
        db_registro.hora_fin = registro_data.hora_fin
        db_registro.horas_trabajadas = registro_data.horas_trabajadas
        db_registro.cantidad_turnos_trabajados = registro_data.cantidad_turnos_trabajados
        db_registro.es_domingo = registro_data.es_domingo
        db_registro.id_maquina = registro_data.id_maquina
        db_registro.id_cliente = registro_data.cliente.id_cliente  # Actualizar el cliente asociado
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

def create_maquina(db: Session, maquina: schemas.MaquinaSchema):
    db_maquina = models.Maquina(
        descripcion_maquina=maquina.descripcion_maquina,
        uso_para_mantenimiento=maquina.uso_para_mantenimiento,
    )
    db.add(db_maquina)
    db.commit()
    db.refresh(db_maquina)
    return db_maquina

# crud.py
def update_maquina(db: Session, id_maquina: int, maquina: schemas.MaquinaBaseSchema):
    db_maquina = db.query(models.Maquina).filter(models.Maquina.id_maquina == id_maquina).first()
    if db_maquina:
        db_maquina.descripcion_maquina = maquina.descripcion_maquina
        db_maquina.uso_para_mantenimiento = maquina.uso_para_mantenimiento
        db.commit()
        db.refresh(db_maquina)
        return db_maquina
    return None

def delete_maquina(db: Session, id_maquina: int):
    db_maquina = get_maquina(db, id_maquina=id_maquina)
    if db_maquina:
        db.delete(db_maquina)
        db.commit()
        return db_maquina
    return None


def get_maquina(db: Session, id_maquina: int):
    return db.query(models.Maquina).filter(models.Maquina.id_maquina == id_maquina).first()


# Crear cliente
def create_cliente(db: Session, cliente: schemas.ClienteCreateSchema):
    db_cliente = models.Cliente(
        nombre_empresa=cliente.nombre_empresa,
        direccion=cliente.direccion,
        telefono=cliente.telefono,
        email=cliente.email
    )
    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)
    return db_cliente

def get_all_clients(db: Session):
    """
    Devuelve todos los clientes registrados en la base de datos.

    Args:
        db (Session): Sesión de la base de datos.

    Returns:
        List[models.Cliente]: Lista de todos los clientes.
    """
    return db.query(models.Cliente).all()


# Obtener cliente por nombre de empresa
def get_cliente(db: Session, nombre_empresa: str):
    return db.query(models.Cliente).filter(models.Cliente.nombre_empresa == nombre_empresa).first()

# Actualizar cliente
def update_cliente(db: Session, id_cliente: int, cliente: schemas.ClienteSchema):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == id_cliente).first()
    if db_cliente:
        db_cliente.nombre_empresa = cliente.nombre_empresa
        db_cliente.direccion = cliente.direccion
        db_cliente.telefono = cliente.telefono
        db_cliente.email = cliente.email
        db.commit()
        db.refresh(db_cliente)
        return db_cliente
    return None

# Borrar cliente
def delete_cliente(db: Session, id_cliente: int):
    db_cliente = db.query(models.Cliente).filter(models.Cliente.id_cliente == id_cliente).first()
    if db_cliente:
        db.delete(db_cliente)
        db.commit()
        return db_cliente
    return None


def get_clients_hours_and_turns(db: Session):
    results = (
        db.query(
            models.Cliente.id_cliente,
            func.sum(models.RegistroHorasTrabajadas.horas_trabajadas).label("total_hours"),
            func.sum(models.RegistroHorasTrabajadas.cantidad_turnos_trabajados).label("total_turns"),
        )
        .join(models.RegistroHorasTrabajadas, models.Cliente.id_cliente == models.RegistroHorasTrabajadas.id_cliente)
        .group_by(models.Cliente.id_cliente)
        .all()
    )

    # Formatea los resultados en un diccionario para fácil acceso
    return {result.id_cliente: {"total_hours": result.total_hours or 0, "total_turns": result.total_turns or 0} for result in results}
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
    total_horas = db.query(func.sum(models.RegistroHorasTrabajadas.horas_trabajadas)).scalar()
    return round(total_horas, 2) if total_horas else 0.00

def get_total_turnos(db: Session):
    return db.query(func.sum(models.RegistroHorasTrabajadas.cantidad_turnos_trabajados)).scalar()

def get_total_permanent_workers(db: Session):
    return db.query(models.Trabajador).filter(models.Trabajador.tipo == "permanente").count()

def get_total_eventual_workers(db: Session):
    return db.query(models.Trabajador).filter(models.Trabajador.tipo == "eventual").count()


# --------- CRUD para Máquinas ---------
def get_machine(db: Session, id_maquina: int):
    return db.query(models.Maquina).filter(models.Maquina.id_maquina == id_maquina).first()

def get_all_machines(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Maquina).offset(skip).limit(limit).all()


def create_machine(db: Session, machine: schemas.MaquinaCreateSchema):
    # Crear la nueva máquina
    db_machine = models.Maquina(
        descripcion_maquina=machine.descripcion_maquina,
        consumo_promedio=machine.consumo_promedio,
        costo_mantenimiento=machine.costo_mantenimiento,
        fecha_instalacion=machine.fecha_instalacion,
        ultima_fecha_mantenimiento=machine.ultima_fecha_mantenimiento,
        tipo_maquina=machine.tipo_maquina,
        tiempo_entre_mantencion=machine.tiempo_entre_mantencion
    )
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine


def update_machine(db: Session, id_maquina: int, machine_data: schemas.MaquinaSchema):
    db_machine = get_machine(db, id_maquina)
    if db_machine:
        db_machine.descripcion_maquina = machine_data.descripcion_maquina
        db_machine.uso_para_mantenimiento = machine_data.uso_para_mantenimiento
        db.commit()
        db.refresh(db_machine)
        return db_machine
    return None

def delete_machine(db: Session, id_maquina: int):
    db_machine = get_machine(db, id_maquina)
    if db_machine:
        db.delete(db_machine)
        db.commit()
        return db_machine
    return None

# --------- Métricas para Máquinas ---------
def get_total_machines(db: Session):
    return db.query(models.Maquina).count()


# Calcular el combustible total consumido por todas las máquinas
def get_total_fuel_consumed(db: Session) -> float:
    """
    Calcula el combustible total consumido por todas las máquinas
    basado en las horas trabajadas y el consumo promedio de cada máquina.
    """
    total_consumo = db.query(
        func.sum(
            RegistroHorasTrabajadas.horas_trabajadas * Maquina.consumo_promedio
        )
    ).join(Maquina, RegistroHorasTrabajadas.id_maquina == Maquina.id_maquina).scalar()

    return total_consumo or 0.0

# Calcular el combustible consumido por máquina
def get_fuel_consumed_per_machine(db: Session) -> list:
    """
    Calcula el combustible consumido por cada máquina.
    Devuelve una lista con la máquina y su consumo total.
    """
    consumos = db.query(
        Maquina.id_maquina,
        Maquina.descripcion_maquina,
        func.sum(RegistroHorasTrabajadas.horas_trabajadas * Maquina.consumo_promedio).label("total_combustible")
    ).join(Maquina, RegistroHorasTrabajadas.id_maquina == Maquina.id_maquina) \
    .group_by(Maquina.id_maquina, Maquina.descripcion_maquina) \
    .all()

    return [
        {"id_maquina": row.id_maquina, "descripcion_maquina": row.descripcion_maquina, "total_combustible": row.total_combustible or 0.0}
        for row in consumos
    ]

def calculate_next_maintenance_date(db: Session, id_maquina: int):
    """
    Calcula la próxima fecha de mantención de una máquina.
    """
    # Obtener la máquina por ID
    maquina = db.query(models.Maquina).filter(models.Maquina.id_maquina == id_maquina).first()
    if not maquina:
        return None  # Retornar None si la máquina no existe
    
    if not maquina.ultima_fecha_mantenimiento or not maquina.tiempo_entre_mantencion:
        return None  # Si falta información, no se puede calcular

    # Calcular la próxima fecha de mantención
    next_maintenance_date = maquina.ultima_fecha_mantenimiento + timedelta(days=maquina.tiempo_entre_mantencion)
    return {"id_maquina": maquina.id_maquina, "descripcion_maquina": maquina.descripcion_maquina, "proxima_fecha_mantenimiento": next_maintenance_date}

def get_registros_horas_trabajadas(db: Session):
    return db.query(models.RegistroHorasTrabajadas).all()
