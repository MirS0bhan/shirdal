from pydantic import BaseModel


class Meta(BaseModel):
    typ: str


class Message(BaseModel):
    _meta: Meta = Meta

