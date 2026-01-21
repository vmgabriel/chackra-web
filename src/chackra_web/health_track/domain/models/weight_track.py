import pydantic
import datetime
import uuid

from chackra_web.shared.domain.model.health_track import weight_track_id
from chackra_web.shared.domain.model.user import user_id



class CreateUserWeightTrack(pydantic.BaseModel):
    user_id: user_id.UserId
    weight: float


class UpdateUserWeightTrack(pydantic.BaseModel):
    user_id: user_id.UserId
    weight: float
    date: datetime.date


class UserWeightTrack(pydantic.BaseModel):
    id: weight_track_id.WeightTrackID
    user_id: user_id.UserId
    weight: float
    date: datetime.date = datetime.date.today()

    active: bool = True
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    deleted_at: datetime.datetime | None = None

    @staticmethod
    def create(create_dto: CreateUserWeightTrack) -> "UserWeightTrack":
        return UserWeightTrack(
            id=weight_track_id.WeightTrackID(value=str(uuid.uuid4())),
            user_id=create_dto.user_id,
            weight=create_dto.weight,
        )

    def update(self, update_dto: UpdateUserWeightTrack) -> "UserWeightTrack":
        self.weight = update_dto.weight
        self.user_id = update_dto.user_id
        self.date = update_dto.date

        self.updated_at = datetime.datetime.now()
        return self
