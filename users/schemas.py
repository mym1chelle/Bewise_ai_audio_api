from pydantic import BaseModel
from uuid import UUID


class ExtendedModel(BaseModel):
    class Config:
        orm_mode = True


class AuthUserModel(ExtendedModel):
    username: str


class TokenDataModel(BaseModel):
    username: str | None = None


class UuidTokenModel(BaseModel):
    uuid: UUID
    token: str
