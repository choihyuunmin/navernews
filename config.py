from pydantic import BaseModel



class PostgresInfo(BaseModel):
    host: str
    port: int
    user: str
    passwd: str