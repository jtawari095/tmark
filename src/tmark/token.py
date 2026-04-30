from pydantic import BaseModel


# Mistune token
class MistuneToken(BaseModel):
    type: str
    raw: str = ""
    style: str | None = None
    children: list["MistuneToken"] = []
    attrs: dict[str, str | int | bool | None] = {}
