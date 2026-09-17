from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import DeclarativeBase,relationship,Mapped,mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    user_id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    email : Mapped[str] = mapped_column(unique=True)
    password_hash : Mapped[str] = mapped_column()
    expenses:Mapped[list["Expense"]] = relationship(
        back_populates="user"
    )

class Category(Base):
    __tablename__ = "categories"
    id : Mapped[int] = mapped_column(primary_key=True)
    name : Mapped[str] = mapped_column()
    expenses : Mapped[list["Expense"]] = relationship(
        back_populates="category"
    )

class Expense(Base):
    __tablename__ = "expenses"
    id : Mapped[int] = mapped_column(primary_key=True)
    amount : Mapped[float] = mapped_column()
    description : Mapped[str] = mapped_column()
    user_id : Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    category_id : Mapped[int] = mapped_column(ForeignKey("categories.id"))
    user :Mapped["User"] = relationship(
        back_populates="expenses"
    )
    category : Mapped["Category"] = relationship(
        back_populates="expenses"
    )