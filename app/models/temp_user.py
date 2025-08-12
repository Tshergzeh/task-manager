from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    hashed_password: str = Field()

class UserLogin(SQLModel):
    username: str
    password: str