from sqlmodel import Session

def save_to_database(model_instance, session: Session):
    session.add(model_instance)
    session.commit()
    session.refresh(model_instance)
    