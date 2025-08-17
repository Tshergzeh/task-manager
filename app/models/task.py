from datetime import datetime, timezone

from sqlmodel import Field, SQLModel, Column, DateTime

class Task(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    title: str = Field()
    description: str | None = Field()
    is_completed: bool = Field(default=False)
    due_date: datetime | None = Field(alias="dueDate")

    created_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            default=lambda: datetime.now(timezone.utc)
        )
    )

    updated_at: datetime = Field(
        sa_column=Column(
            DateTime(timezone=True), 
            default=lambda: datetime.now(timezone.utc), 
            onupdate=lambda: datetime.now(timezone.utc)
        )
    )
    
    owner: str = Field(foreign_key="user.username")

class TaskComplete(SQLModel):
    id: int
    is_completed: bool = True
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
