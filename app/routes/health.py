from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.database import database_health_check, get_session

router = APIRouter()

@router.get("/api/health", tags=["health"])
def health_check(session: Session = Depends(get_session)):
    checks = {
        "database": database_health_check(session)()
    }
    status_code = 200 if all(checks.values()) else 503
    if status_code == 200: 
        return checks
    else:
        return {
            "status": "unhealthy", 
            "checks": checks
        }