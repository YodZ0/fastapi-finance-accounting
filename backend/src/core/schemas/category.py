from enum import Enum
from pydantic import BaseModel, ConfigDict


class CategoryType(str, Enum):
    EXPENSE: str = "EXPENSE"
    INCOME: str = "INCOME"
    SAVING: str = "SAVING"


class CategoryBase(BaseModel):
    name: str
    type: CategoryType


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
