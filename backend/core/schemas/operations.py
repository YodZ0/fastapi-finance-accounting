from enum import Enum
import datetime

from pydantic import BaseModel, Field


class OperationKind(str, Enum):
    INCOME: str = 'INCOME'
    EXPENSE: str = 'EXPENSE'


class Currency(str, Enum):
    KZT: str = 'KZT'
    RUB: str = 'RUB'
    USD: str = 'USD'
    EUR: str = 'EUR'


class OperationBase(BaseModel):
    id: int
    title: str = Field(max_length=50)
    amount: float = Field(ge=0)
    currency: Currency
    kind: OperationKind
    date: datetime.date = datetime.date.today


class OperationCreate(BaseModel):
    title: str = Field(max_length=50)
    amount: float = Field(ge=0)
    currency: Currency
    kind: OperationKind
    date: datetime.date = datetime.date.today


class OperationRead(OperationBase):
    pass
