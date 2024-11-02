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
    hora_inicio = Column(Time)  # Agregamos la hora de inicio
    hora_fin = Column(Time)      # Agregamos la hora final
    horas_trabajadas = Column(Float)  # Este campo será calculado
    cantidad_turnos_trabajados = Column(Float)
    es_domingo = Column(Boolean, default=False)  # Campo booleano para determinar si es domingo

    trabajador = relationship("Trabajador", back_populates="registros")
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
    descripcion_maquina = Column(String)
    uso_para_mantenimiento = Column(String)

    mantenimientos = relationship("Mantenimiento", back_populates="maquina")

class Sueldo(Base):
    __tablename__ = "sueldos"
    id_sueldo = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_trabajador = Column(Integer, ForeignKey("trabajadores.id_trabajador"))
    fecha = Column(DateTime)

    trabajador = relationship("Trabajador", back_populates="sueldos")