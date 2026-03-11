from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import EmailStr
from app.core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

async def send_reset_email(email: EmailStr, token: str):

    reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    html = f"""
    <h2>Recuperar contraseña</h2>
    <p>Haz clic en el siguiente enlace para cambiar tu contraseña:</p>
    <a href="{reset_link}">{reset_link}</a>
    <p>Este enlace expira en 1 hora.</p>
    """

    message = MessageSchema(
        subject="Recuperación de contraseña",
        recipients=[email],
        body=html,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)