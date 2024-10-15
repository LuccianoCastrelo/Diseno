from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Float
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
    turnos = relationship("Turno", back_populates="trabajador")
    registros = relationship("RegistroHorasTrabajadas", back_populates="trabajador")
    sueldos = relationship("Sueldo", back_populates="trabajador")   

class Turno(Base):
    __tablename__ = "turnos"
    id_turno = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_trabajador = Column(Integer, ForeignKey("trabajadores.id_trabajador"))
    hora_inicio = Column(DateTime)
    hora_fin = Column(DateTime)
    duracion = Column(Integer)

    trabajador = relationship("Trabajador", back_populates="turnos")
    registros = relationship("RegistroHorasTrabajadas", back_populates="turno")

class RegistroHorasTrabajadas(Base):
    __tablename__ = "registro_horas_trabajadas"
    id_registro = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_trabajador = Column(Integer, ForeignKey("trabajadores.id_trabajador"))
    id_turno = Column(Integer, ForeignKey("turnos.id_turno"))
    fecha = Column(Date)
    horas_trabajadas = Column(Integer)
    cantidad_turnos_trabajados = Column(Float)

    trabajador = relationship("Trabajador", back_populates="registros")
    turno = relationship("Turno", back_populates="registros")

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
