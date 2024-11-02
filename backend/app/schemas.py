
from pydantic import BaseModel
from typing import Optional,List
from datetime import datetime, date,time

#ESTOS SON DE LA BASE DE DATOS

class AdministradorSchema(BaseModel):
    id_administrador: int
    nombre: str
    correo: str

    class Config:
        from_attributes = True

class TrabajadorSchemaReq(BaseModel):
    nombre: str
    tipo: str
    pago_por_turno: int
    salario_base: Optional[int] = None  # Hacer opcional para trabajadores eventuales    
    rut: str  # Añadir el campo RUT

    class Config:
        from_attributes = True

class TrabajadorSchema(TrabajadorSchemaReq):
    id_trabajador: int

    class Config:
        from_attributes = True
# Schema para crear un registro (sin el cálculo de horas trabajadas)
class RegistroHorasTrabajadasCreateSchema(BaseModel):
    id_trabajador: int
    fecha: date
    hora_inicio: time  # Agregamos la hora de inicio
    hora_fin: time      # Agregamos la hora final
# Schema para lectura, que incluye el cálculo de horas trabajadas
class RegistroHorasTrabajadasSchema(BaseModel):
    id_registro: int
    id_trabajador: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    horas_trabajadas: float  # Ahora esto se calculará en el backend
    cantidad_turnos_trabajados: float
    es_domingo: bool  # Nuevo campo que indica si la fecha es domingo

    class Config:
        orm_mode = True
# Esquema para devolver listas de registros
class RegistroHorasTrabajadasListResponse(BaseModel):
    registros: List[RegistroHorasTrabajadasSchema]

class MantenimientoSchema(BaseModel):
    id_mantenimiento: int
    id_maquina: int
    fecha: datetime
    tipo_mantenimiento: str

    class Config:
        from_attributes = True

class MaquinaSchema(BaseModel):
    id_maquina: int
    descripcion_maquina: str
    uso_para_mantenimiento: str

    class Config:
        from_attributes = True

class SueldoSchema(BaseModel):
    id_sueldo: int
    id_trabajador: int
    fecha: date

    class Config:
        from_attributes = True
class RegistroIds(BaseModel):
    ids: List[int]
class SueldoMensualResponse(BaseModel):
    sueldo_mensual: int

