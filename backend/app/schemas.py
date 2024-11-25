
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
class RegistroHorasTrabajadasCreateSchema(BaseModel):
    id_trabajador: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    id_maquina: Optional[int] = None  # Campo opcional para asociar una máquina

# Esquema para la lectura de registros (actualizado)
class RegistroHorasTrabajadasSchema(BaseModel):
    id_registro: int
    id_trabajador: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    horas_trabajadas: float
    cantidad_turnos_trabajados: float
    es_domingo: bool
    id_maquina: Optional[int] = None  # Incluir máquina en el esquema de salida

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
        
class MaquinaCreateSchema(BaseModel):
    descripcion_maquina: str
    uso_para_mantenimiento: str

class MaquinaSchema(MaquinaCreateSchema):
    id_maquina: int

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

