from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: float
    description: str | None = None
    category_id: int


class ExpenseUpdate(BaseModel):
    amount: float | None = None
    description: str | None = None
    category_id: int | None = None


class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str


class UserLogin(BaseModel):
    email: str
    password: str