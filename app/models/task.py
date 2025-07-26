from datetime import datetime

from sqlmodel import Field, SQLModel

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str = Field()
    description: str | None = Field()
    is_completed: bool = Field(default=False)
    due_date: datetime | None = Field()
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    owner: str = Field(foreign_key="user.username")

class TaskUpdate(SQLModel):
    title: str | None
    description: str | None
    is_completed: bool | None
    due_date: datetime | None
    updated_at: datetime = datetime.now()