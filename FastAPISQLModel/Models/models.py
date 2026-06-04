from sqlmodel import Field, SQLModel


class Data(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    secret_name: str
    age: int | None = Field(default=None, index=True)
    
#class DataCreate(SQLModel):
    #pass

#class DataPublic(SQLModel):
    #id: int

