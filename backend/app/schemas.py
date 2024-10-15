
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

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

class TurnoSchema(BaseModel):
    id_turno: int
    id_trabajador: int
    hora_inicio: datetime
    hora_fin: datetime
    duracion: int

    class Config:
        from_attributes = True

class RegistroHorasTrabajadasSchema(BaseModel):
    id_registro: int
    id_trabajador: int
    id_turno: int
    fecha: date
    horas_trabajadas: int
    cantidad_turnos_trabajados: float

    class Config:
        from_attributes = True

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