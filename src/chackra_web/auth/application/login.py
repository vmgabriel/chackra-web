import pydantic


class LoginDTO(pydantic.BaseModel):
    email: str
    password: str

    def verify(self) -> bool:
        return self.email == "test@test.com" and self.password == "test"



class LoginCommand:
    def __init__(self, requirements: ...) -> None:
        ...

    def execute(self, login_data: LoginDTO) -> bool:
        return login_data.verify()