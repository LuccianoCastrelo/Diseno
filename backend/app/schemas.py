
from pydantic import BaseModel
from datetime import datetime, date
#ESTOS SON EJEMPLOS
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True


#ESTOS SON DE LA BASE DE DATOS

class AdministradorSchema(BaseModel):
    id_administrador: int
    nombre: str
    correo: str

    class Config:
        orm_mode = True

class TrabajadorSchema(BaseModel):
    id_trabajador: int
    nombre: str

    class Config:
        orm_mode = True

class TurnoSchema(BaseModel):
    id_turno: int
    id_trabajador: int
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
