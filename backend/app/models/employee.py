from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.account import Account


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), unique=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))

    account: Mapped["Account"] = relationship(back_populates="employee")
