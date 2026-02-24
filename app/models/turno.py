from sqlalchemy import Column, Date, Time, ForeignKey, Integer, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import String
import uuid
from sqlalchemy import Enum as SQLEnum

from app.db.base import Base
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

    tipo_turno = Column(Integer, nullable=False)

    

    estado = Column(
        SQLEnum(
            "Abierto",
            "confirmado",
            "cancelado",
            "completado",
            name="estado_turno_enum",
            create_type=False,
            native_enum=True,
            validate_strings=True
        ),
        nullable=False,
        server_default="Abierto"
    )

    fecha = Column(Date, nullable=False)

    hora_inicio = Column(Time, nullable=False)

    hora_fin = Column(Time, nullable=False)
    
    rango_horario = Column(String(2), nullable=False)

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
