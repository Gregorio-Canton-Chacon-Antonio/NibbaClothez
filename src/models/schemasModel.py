from pydantic import BaseModel
from typing import Optional


class UsuarioShema(BaseModel):
    nombre: str
    email: str
    password: str


class PrendaSchema(BaseModel):
    titulo: str
    precio: float
    talla: str
    condicion: str
    marca: Optional[str] = "Sin marca"
    descripcion: Optional[str] = None