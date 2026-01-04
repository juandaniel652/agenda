#from fastapi import APIRouter, Depends
#from sqlalchemy.orm import Session
#from sqlalchemy import text
#
#from app.api.deps import get_db
#
#
#router = APIRouter(
#    prefix="/health",
#    tags=["Health"]
#)
#
#@router.get("/")
#def health_check():
#    return {"status": "ok"}
#
#@router.get("/db")
#def db_check(db: Session = Depends(get_db)):
#    db.execute(text("SELECT 1"))
#    return {
#        "status": "ok",
#        "database": "connected"
#    }

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"]
)

@router.get("")
def health_check():
    return {"status": "ok"}
