import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class PeriodBase(BaseModel):
    start: datetime.date
    end: datetime.date
    name: str
    user_id: uuid.UUID


class PeriodCreate(PeriodBase):
    pass


class Period(PeriodBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
