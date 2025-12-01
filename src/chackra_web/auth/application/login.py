import pydantic


class LoginValueObject(pydantic.BaseModel):
    email: str
    password: str

    def verify(self) -> bool:
        return self.email == "test" and self.password == "test"



class LoginCommand:
    def __init__(self, requirements: ...) -> None:
        ...

    def execute(self, login_data: LoginValueObject) -> bool:
        return login_data.verify()