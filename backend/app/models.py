from sqlalchemy.ext.declarative import declarative_base
#ESTAS SON LAS TABLAS DE LA BASE DE DATOS
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base  # Asegúrate de tener esta importación correcta

#ESTE ES SOLO UN EJEMPLO
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

#Estos son los modelos de la base de datos
class Administrador(Base):
    __tablename__ = "administradores"  # Ajuste a plural para mantener consistencia
    id_administrador = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    correo = Column(String)

class Trabajador(Base):
    __tablename__ = "trabajadores"
    id_trabajador = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)

class Turno(Base):
    __tablename__ = "turnos"
    id_turno = Column(Integer, primary_key=True, index=True)
    id_trabajador = Column(Integer, ForeignKey("trabajadores.id_trabajador"))
    hora_inicio = Column(DateTime)
    hora_fin = Column(DateTime)
    duracion = Column(Integer)

    trabajador = relationship("Trabajador", back_populates="turnos")

class RegistroHorasTrabajadas(Base):
    __tablename__ = "registro_horas_trabajadas"
    id_registro = Column(Integer, primary_key=True, index=True)
    id_trabajador = Column(Integer, ForeignKey("trabajadores.id_trabajador"))
    id_turno = Column(Integer, ForeignKey("turnos.id_turno"))
    fecha = Column(Date)
    horas_trabajadas = Column(Integer)

    trabajador = relationship("Trabajador", back_populates="registros")
    turno = relationship("Turno", back_populates="registros")

class Mantenimiento(Base):
    __tablename__ = "mantenimientos"
    id_mantenimiento = Column(Integer, primary_key=True, index=True)
    id_maquina = Column(Integer, ForeignKey("maquinas.id_maquina"))
    fecha = Column(DateTime)
    tipo_mantenimiento = Column(String)

    maquina = relationship("Maquina", back_populates="mantenimientos")

class Maquina(Base):
    __tablename__ = "maquinas"
    id_maquina = Column(Integer, primary_key=True, index=True)
    descripcion_maquina = Column(String)
    uso_para_mantenimiento = Column(String)

    mantenimientos = relationship("Mantenimiento", back_populates="maquina")

# Relaciones en Trabajador
Trabajador.turnos = relationship("Turno", back_populates="trabajador")
Trabajador.registros = relationship("RegistroHorasTrabajadas", back_populates="trabajador")

# Relaciones en Turno
Turno.registros = relationship("RegistroHorasTrabajadas", back_populates="turno")
