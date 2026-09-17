from fastapi import FastAPI, Depends, HTTPException
from .database import get_session
from sqlalchemy.orm import Session
from .schemas import (
    ExpenseCreate,
    ExpenseUpdate,
    UserCreate,
    UserUpdate,
    UserResponse,
    CategoryCreate,
    CategoryUpdate,
    UserLogin
)
from .models import Expense, User, Category
from sqlalchemy import select
from .auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    verify_access_token
)
from fastapi.security import OAuth2PasswordBearer


app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    return payload


@app.get("/")
def root():
    return {"Hello": "World"}


# =========================
# USERS
# =========================

@app.get("/users", response_model=list[UserResponse])
def get_users(session: Session = Depends(get_session)):
    data = session.scalars(select(User)).all()
    return data


@app.post("/users", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@app.get("/users/{users_id}", response_model=UserResponse)
def get_user(
    users_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, users_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@app.patch("/users/{users_id}", response_model=UserResponse)
def update_user(
    users_id: int,
    user_data: UserUpdate,
    session: Session = Depends(get_session)
):
    user = session.get(User, users_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user_data.name is not None:
        user.name = user_data.name

    if user_data.email is not None:
        user.email = user_data.email

    session.commit()
    session.refresh(user)

    return user


@app.delete("/users/{users_id}")
def delete_user(
    users_id: int,
    session: Session = Depends(get_session)
):
    user = session.get(User, users_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    session.delete(user)
    session.commit()

    return {"message": "User deleted"}


# =========================
# CATEGORIES
# =========================

@app.get("/categories")
def get_categories(session: Session = Depends(get_session)):
    data = session.scalars(select(Category)).all()
    return data


@app.post("/categories")
def create_category(
    category: CategoryCreate,
    session: Session = Depends(get_session)
):
    new_category = Category(
        name=category.name
    )

    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return new_category


@app.get("/categories/{category_id}")
def get_category(
    category_id: int,
    session: Session = Depends(get_session)
):
    category = session.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return category


@app.patch("/categories/{category_id}")
def update_category(
    category_id: int,
    category_data: CategoryUpdate,
    session: Session = Depends(get_session)
):
    category = session.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    category.name = category_data.name

    session.commit()
    session.refresh(category)

    return category


@app.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    session: Session = Depends(get_session)
):
    category = session.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    session.delete(category)
    session.commit()

    return {"message": "Category deleted"}


# =========================
# EXPENSES
# =========================

@app.get("/expenses")
def get_expenses(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    data = session.scalars(
        select(Expense).where(
            Expense.user_id == user_id
        )
    ).all()

    return data


@app.post("/expenses")
def create_expense(
    expense: ExpenseCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    category = session.get(Category, expense.category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    new_expense = Expense(
        amount=expense.amount,
        description=expense.description,
        user_id=user_id,
        category_id=expense.category_id
    )

    session.add(new_expense)
    session.commit()
    session.refresh(new_expense)

    return new_expense


@app.get("/expenses/{expense_id}")
def get_expense(
    expense_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    expense = session.scalars(
        select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id
        )
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return expense


@app.patch("/expenses/{expense_id}")
def update_expense(
    expense_id: int,
    expense_data: ExpenseUpdate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    expense = session.scalars(
        select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id
        )
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    if expense_data.category_id is not None:
        category = session.get(Category, expense_data.category_id)

        if category is None:
            raise HTTPException(
                status_code=404,
                detail="Category not found"
            )

        expense.category_id = expense_data.category_id

    if expense_data.amount is not None:
        expense.amount = expense_data.amount

    if expense_data.description is not None:
        expense.description = expense_data.description

    session.commit()
    session.refresh(expense)

    return expense


@app.delete("/expenses/{expense_id}")
def delete_expense(
    expense_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user)
):
    user_id = int(current_user["sub"])

    expense = session.scalars(
        select(Expense).where(
            Expense.id == expense_id,
            Expense.user_id == user_id
        )
    ).first()

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    session.delete(expense)
    session.commit()

    return {"message": "Expense deleted"}


# =========================
# LOGIN
# =========================

@app.post("/login")
def login(
    user_data: UserLogin,
    session: Session = Depends(get_session)
):
    data = session.scalars(
        select(User).where(
            User.email == user_data.email
        )
    ).first()

    if data is None:
        return "Email or Password Is Incorrect"

    password_1 = verify_password(
        user_data.password,
        data.password_hash
    )

    if password_1 is False:
        return "Email Or password is incorrect"

    details = {
        "sub": str(data.user_id)
    }

    access_token = create_access_token(details)

    return access_token