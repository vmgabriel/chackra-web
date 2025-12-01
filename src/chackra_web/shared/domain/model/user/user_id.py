import pydantic


class UserId(pydantic.BaseModel):
    value: str