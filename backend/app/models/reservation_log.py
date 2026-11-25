from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Enum, ForeignKey, Identity, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enum_type import LogEventType

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.reservation import Reservation


class ReservationLog(Base):
    __tablename__ = "reservation_logs"
    __table_args__ = (
        Index(
            "ix_reservation_logs_reservation_id_changed_at",
            "reservation_id",
            "changed_at",
        ),
    )

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id"))
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    event_type: Mapped[LogEventType] = mapped_column(
        Enum(
            LogEventType,
            name="log_event_type",
            values_callable=lambda enum_cls: [log_type.value for log_type in enum_cls],
        )
    )
    field_name: Mapped[str | None] = mapped_column(String(50))
    old_value: Mapped[str | None] = mapped_column(Text)
    new_value: Mapped[str | None] = mapped_column(Text)

    account: Mapped["Account"] = relationship()

    reservation: Mapped["Reservation"] = relationship(back_populates="logs")
