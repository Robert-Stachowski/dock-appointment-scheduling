from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, Identity, String, Text, false, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enum_type import AccountRole

if TYPE_CHECKING:
    from app.models.employee import Employee


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    email: Mapped[str] = mapped_column(String(254), unique=True)
    hashed_password: Mapped[str] = mapped_column(Text)
    role: Mapped[AccountRole] = mapped_column(
        Enum(
            AccountRole,
            name="account_role",
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        )
    )
    is_active: Mapped[bool] = mapped_column(server_default=false())
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    employee: Mapped["Employee | None"] = relationship(back_populates="account")

    def __repr__(self) -> str:
        return f"Konto: {self.id} - {self.email}, rola: {self.role}"
