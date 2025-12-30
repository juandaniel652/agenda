from sqlalchemy import Column, Integer, String
from app.db import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    numero_cliente = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    domicilio = Column(String, nullable=False)
    numero_domicilio = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
