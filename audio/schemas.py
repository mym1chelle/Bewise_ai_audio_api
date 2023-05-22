from pydantic import BaseModel


class ExtendedModel(BaseModel):
    class Config:
        orm_mode = True


class SendLinkModel(ExtendedModel):
    link: str
