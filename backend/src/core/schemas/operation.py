import datetime
import uuid
from enum import Enum
from pydantic import BaseModel, ConfigDict


class Currency(str, Enum):
    KZT: str = "KZT"
    RUB: str = "RUB"
    USD: str = "USD"
    EUR: str = "EUR"
    KRW: str = "KRW"


class OperationBase(BaseModel):
    name: str
    amount: float
    currency: Currency
    date: datetime.date
    category_id: int
    period_id: int


class OperationCreate(OperationBase):
    pass


class Operation(OperationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: uuid.UUID
