from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date
#ESTOS SON DE LA BASE DE DATOS

class AdministradorSchema(BaseModel):
    id_administrador: int
    nombre: str
    correo: str

    class Config:
        orm_mode = True

class TrabajadorSchemaReq(BaseModel):
    nombre: str
    tipo: str
    pago_por_turno: int
    salario_base: Optional[int] = None  # Hacer opcional para trabajadores eventuales    
    rut: str  # Añadir el campo RUT

    class Config:
        orm_mode = True

class TrabajadorSchema(TrabajadorSchemaReq):
    id_trabajador: int
class TurnoSchema(BaseModel):
    id_turno: int
    hora_inicio: datetime
    hora_fin: datetime
    duracion: int

    class Config:
        orm_mode = True
class RegistroHorasTrabajadasSchema(BaseModel):
    id_registro: int
    id_trabajador: int
    id_turno: int
    fecha: date
    horas_trabajadas: int
    cantidad_turnos_trabajados: float

    class Config:
        orm_mode = True

class MantenimientoSchema(BaseModel):
    id_mantenimiento: int
    id_maquina: int
    fecha: datetime
    tipo_mantenimiento: str

    class Config:
        orm_mode = True

class MaquinaSchema(BaseModel):
    id_maquina: int
    descripcion_maquina: str
    uso_para_mantenimiento: str

    class Config:
        orm_mode = True
