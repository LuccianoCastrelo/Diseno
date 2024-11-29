#models.py
from sqlalchemy import Column, Integer, String, Date, DateTime,Time, ForeignKey, Float,Boolean
from sqlalchemy.orm import relationship
from .database import Base

class Administrador(Base):
    __tablename__ = "administradores"
    id_administrador = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String)
    correo = Column(String)

class Trabajador(Base): 
    __tablename__ = "trabajadores"
    id_trabajador = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String)
    tipo = Column(String)  # 'eventual' o 'permanente'
    pago_por_turno = Column(Integer)
    salario_base = Column(Integer, nullable=True)  # Permitir que sea nulo para trabajadores eventuales
    rut = Column(String, unique=True, index=True)
    
    # Relaciones
    registros = relationship("RegistroHorasTrabajadas", back_populates="trabajador")
    sueldos = relationship("Sueldo", back_populates="trabajador")   

class RegistroHorasTrabajadas(Base):
    __tablename__ = "registro_horas_trabajadas"

    id_registro = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_trabajador = Column(Integer, ForeignKey("trabajadores.id_trabajador"))
    fecha = Column(Date)
    hora_inicio = Column(Time)
    hora_fin = Column(Time)
    horas_trabajadas = Column(Float)
    cantidad_turnos_trabajados = Column(Float)
    es_domingo = Column(Boolean, default=False)
    id_maquina = Column(Integer, ForeignKey("maquinas.id_maquina"), nullable=True)
    id_cliente = Column(Integer, ForeignKey("clientes.id_cliente"), nullable=False)  # Relación obligatoria con cliente

    # Relaciones
    trabajador = relationship("Trabajador", back_populates="registros")
    maquina = relationship("Maquina")  # Relación con la tabla de máquinas
    cliente = relationship("Cliente", back_populates="registros")  # Relación con el cliente

class Mantenimiento(Base):
    __tablename__ = "mantenimientos"
    id_mantenimiento = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_maquina = Column(Integer, ForeignKey("maquinas.id_maquina"))
    fecha = Column(DateTime)
    tipo_mantenimiento = Column(String)

    maquina = relationship("Maquina", back_populates="mantenimientos")

class Maquina(Base):
    __tablename__ = "maquinas"

    id_maquina = Column(Integer, primary_key=True, index=True, autoincrement=True)
    descripcion_maquina = Column(String, nullable=False)  # Descripción general
    consumo_promedio = Column(Float, nullable=True)  # Consumo promedio (en kWh o cualquier unidad relevante)
    costo_mantenimiento = Column(Float, nullable=True)  # Costo total de mantenimiento en el último año
    fecha_instalacion = Column(Date, nullable=True)  # Fecha de instalación
    ultima_fecha_mantenimiento = Column(Date, nullable=True)  # Fecha del último mantenimiento
    tipo_maquina = Column(String, nullable=True)  # Tipo o categoría de la máquina
    tiempo_entre_mantencion = Column(Integer, nullable=True)

    # Relación con Mantenimiento    
    mantenimientos = relationship("Mantenimiento", back_populates="maquina")
class Sueldo(Base):
    __tablename__ = "sueldos"
    id_sueldo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_trabajador = Column(Integer, ForeignKey("trabajadores.id_trabajador"))
    fecha = Column(DateTime)

    trabajador = relationship("Trabajador", back_populates="sueldos")

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre_empresa = Column(String, nullable=False)
    direccion = Column(String, nullable=True)
    telefono = Column(String, nullable=True)
    email = Column(String, nullable=True)

    # Relación con registros de horas trabajadas (habilitar cascada)
    registros = relationship(
        "RegistroHorasTrabajadas",
        back_populates="cliente",
        cascade="all, delete"
    )
