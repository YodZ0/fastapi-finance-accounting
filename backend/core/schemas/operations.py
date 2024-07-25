from enum import Enum
from datetime import date

from pydantic import BaseModel, Field


class OperationKind(Enum):
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'


class Currency(Enum):
    KZT = 'KZT'
    RUB = 'RUB'
    USD = 'USD'
    EUR = 'EUR'


class OperationBase(BaseModel):
    id: int
    title: str = Field(max_length=50)
    amount: float = Field(ge=0)
    currency: Currency
    kind: OperationKind
    date: date = date.today


class OperationCreate(OperationBase):
    pass


class OperationRead(OperationBase):
    pass
