from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base
import uuid

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero_cliente = Column(Integer, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    domicilio = Column(String, nullable=False)
    numero_domicilio = Column(Integer, nullable=False)
    email = Column(String, unique=True, nullable=False)
