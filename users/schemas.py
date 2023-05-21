from pydantic import BaseModel


class ExtendedModel(BaseModel):
    class Config:
        orm_mode = True


class AuthUserModel(ExtendedModel):
    username: str


class TokenDataModel(BaseModel):
    username: str | None = None
