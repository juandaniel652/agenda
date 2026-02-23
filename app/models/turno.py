from sqlalchemy import Column, Date, Time, Enum, ForeignKey, Integer, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import String
import uuid

from app.db.base import Base
from app.schemas.turno import TipoTurnoEnum
from sqlalchemy import DateTime


class Turno(Base):
    __tablename__ = "turnos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    numero_ticket = Column(String, nullable=False, index=True)

    cliente_id = Column(
        UUID(as_uuid=True),
        ForeignKey("clientes.id", ondelete="RESTRICT"),
        nullable=False
    )

    tecnico_id = Column(
        UUID(as_uuid=True),
        ForeignKey("tecnicos.id", ondelete="RESTRICT"),
        nullable=False
    )

    tipo_turno = Column(Enum(TipoTurnoEnum, name="tipo_turno_enum"), nullable=False)

    estado = Column(
        Enum("pendiente", "confirmado", "cancelado", "completado", name="estado_turno_enum"),
        nullable=False,
        server_default="pendiente"
    )

    fecha = Column(Date, nullable=False)

    hora_inicio = Column(Time, nullable=False)

    hora_fin = Column(Time, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("now()")
    )
    
    cancelado_en = Column(
        DateTime(timezone=True),
        nullable=True
    )

    cancelado_por = Column(
        UUID(as_uuid=True),
        ForeignKey("tecnicos.id", ondelete="SET NULL"),
        nullable=True
    )

    cliente = relationship("Cliente", foreign_keys=[cliente_id])

    tecnico = relationship("Tecnico", foreign_keys=[tecnico_id])

    cancelador = relationship("Tecnico", foreign_keys=[cancelado_por])
