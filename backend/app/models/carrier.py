from typing import TYPE_CHECKING

from sqlalchemy import CHAR, CheckConstraint, ForeignKey, Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.account import Account


class Carrier(Base):
    __tablename__ = "carriers"
    __table_args__ = (
        CheckConstraint("nip ~ '^[0-9]{10}$'", name="ck_carriers_nip_digits"),
    )

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"), unique=True)
    company_name: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(150))
    nip: Mapped[str] = mapped_column(CHAR(10), unique=True)
    phone: Mapped[str] = mapped_column(String(20), unique=True)

    account: Mapped["Account"] = relationship(back_populates="carrier")
