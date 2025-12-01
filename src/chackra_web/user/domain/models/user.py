import pydantic

from chackra_web.shared.domain.model.user import user_id as domain_user_id


class User(pydantic.BaseModel):
    id: domain_user_id.UserId
    name: str
    last_name: str
    email: str