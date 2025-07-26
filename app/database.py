from sqlmodel import create_engine, select, Session, SQLModel

from app.config import settings
from app.models import user, task

DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL)

def create_database_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
        
def database_health_check(session: Session):
    def checker():
        try:
            session.exec(select(1))
            return True
        except Exception as e:
            return False
    
    return checker