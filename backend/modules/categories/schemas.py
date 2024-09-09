from enum import Enum
from pydantic import BaseModel, ConfigDict


class CategoryType(str, Enum):
    EXPENSE = 'Expense'
    INCOME = 'Income'
    INVESTMENT = 'Investment'
    SAVING = 'Saving'


class CategoryBase(BaseModel):
    name: str
    type: CategoryType


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
