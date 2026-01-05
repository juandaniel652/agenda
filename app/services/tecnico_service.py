from app.schemas.tecnico import TecnicoCreate
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password
from app.db.session import SessionLocal

class TecnicoService:

    @staticmethod
    def crear_tecnico(data: TecnicoCreate):
        db = SessionLocal()

        try:
            # Verificar si ya existe
            existing = UserRepository.get_by_email(db, data.email)
            if existing:
                raise ValueError("El usuario ya existe")

            user = UserRepository.create(
                db,
                email=data.email,
                password_hash=hash_password(data.password),
                role="tecnico",
                is_active=True,
                is_verified=True
            )

            return {
                "id": str(user.id),
                "email": user.email,
                "role": user.role
            }

        finally:
            db.close()
