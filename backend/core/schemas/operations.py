from enum import Enum
import datetime
from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


class OperationKind(str, Enum):
    INCOME: str = 'INCOME'
    EXPENSE: str = 'EXPENSE'


class Currency(str, Enum):
    KZT: str = 'KZT'
    RUB: str = 'RUB'
    USD: str = 'USD'
    EUR: str = 'EUR'


class IncomeCategories(str, Enum):
    SALARY: str = 'SALARY'
    BONUSES: str = 'BONUSES'
    SIDE: str = 'SIDE'
    PASSIVE: str = 'PASSIVE'
    GIFTS: str = 'GIFTS'
    OTHER: str = 'OTHER'


class ExpenseCategories(str, Enum):
    FOOD: str = 'FOOD'
    HOUSING: str = 'HOUSING'
    TRANSPORT: str = 'TRANSPORT'
    INTERNET: str = 'INTERNET'
    ENTERTAINMENT: str = 'ENTERTAINMENT'
    CLOTHES: str = 'CLOTHES'
    HEALTH: str = 'HEALTH'
    EDUCATION: str = 'EDUCATION'
    GIFTS: str = 'GIFTS'
    VACATION: str = 'VACATION'
    OTHER: str = 'OTHER'


class OperationBase(BaseModel):
    id: int
    title: str = Field(max_length=50)
    amount: float = Field(ge=0)
    currency: Currency
    kind: OperationKind
    category: Union[IncomeCategories, ExpenseCategories]
    date: datetime.date = datetime.date.today


class OperationCreate(BaseModel):
    title: str = Field(max_length=50)
    amount: float = Field(ge=0)
    currency: Currency
    kind: OperationKind
    category: Union[IncomeCategories, ExpenseCategories]
    date: datetime.date = datetime.date.today

    @field_validator('category', mode='after')
    def validate_category(cls, cat, info: ValidationInfo):
        kind = info.data.get('kind')
        if kind == 'INCOME' and not isinstance(cat, IncomeCategories):
            raise ValueError('Invalid category for INCOME operation')
        elif kind == 'EXPENSE' and not isinstance(cat, ExpenseCategories):
            raise ValueError('Invalid category for EXPENSE operation')
        return cat


class OperationFilter(BaseModel):
    currency: Optional[Currency] = None
    date_start: Optional[datetime.date] = None
    date_end: Optional[datetime.date] = None
    kind: Optional[OperationKind] = None
    category: Optional[Union[IncomeCategories, ExpenseCategories]] = None


class OperationRead(OperationBase):
    pass
