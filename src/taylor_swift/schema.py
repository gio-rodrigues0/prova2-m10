from pydantic import BaseModel

class TSSongs(BaseModel):
    id: int
    title: str
    album: str