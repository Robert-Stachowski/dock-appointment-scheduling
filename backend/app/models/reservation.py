from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Enum,
    ForeignKey,
    Identity,
    Index,
    SmallInteger,
    String,
    func,
    literal_column,
    text,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import constants
from app.core.database import Base
from app.models.enum_type import ReservationStatus

if TYPE_CHECKING:
    from app.models.account import Account
    from app.models.carrier import Carrier
    from app.models.ramp import Ramp
    from app.models.reservation_log import ReservationLog


class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = (
        CheckConstraint(
            f"pallet_count BETWEEN {constants.MIN_PALLETS} AND {constants.MAX_PALLETS}",
            name="ck_reservations_pallet_count",
        ),
        CheckConstraint("start_at < end_at", name="ck_reservations_time_order"),
        CheckConstraint(
            f"((status = '{ReservationStatus.CANCELLED}') = "
            "(cancelled_by IS NOT NULL))"
            f" AND ((status = '{ReservationStatus.CANCELLED}') = "
            "(cancelled_at IS NOT NULL))",
            name="ck_reservations_cancel_consistency",
        ),
        ExcludeConstraint(
            ("ramp_id", "="),
            (
                func.tstzrange(literal_column("start_at"), literal_column("end_at")),
                "&&",
            ),
            using="gist",
            where=text(f"status <> '{ReservationStatus.CANCELLED}'"),
            name="ex_reservations_ramp_overlap",
        ),
        Index("ix_reservations_carrier_id_start_at", "carrier_id", "start_at"),
    )

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    carrier_id: Mapped[int] = mapped_column(ForeignKey("carriers.id"))
    ramp_id: Mapped[int] = mapped_column(ForeignKey("ramps.id"))
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    pallet_count: Mapped[int] = mapped_column(SmallInteger)
    product_description: Mapped[str] = mapped_column(String(100))
    driver_first_name: Mapped[str] = mapped_column(String(50))
    driver_last_name: Mapped[str] = mapped_column(String(50))
    registration_number: Mapped[str] = mapped_column(String(15))
    driver_phone: Mapped[str] = mapped_column(String(20))
    status: Mapped[ReservationStatus] = mapped_column(
        Enum(
            ReservationStatus,
            name="reservation_status",
            values_callable=lambda enum_cls: [rstatus.value for rstatus in enum_cls],
        ),
        server_default=ReservationStatus.PENDING.value,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_by: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"))
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    cancelled_by: Mapped[int | None] = mapped_column(ForeignKey("accounts.id"))
    cancelled_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    updated_by_account: Mapped["Account | None"] = relationship(
        foreign_keys=[updated_by]
    )
    cancelled_by_account: Mapped["Account | None"] = relationship(
        foreign_keys=[cancelled_by]
    )

    carrier: Mapped["Carrier"] = relationship(back_populates="reservations")
    ramp: Mapped["Ramp"] = relationship(back_populates="reservations")
    logs: Mapped[list["ReservationLog"]] = relationship(back_populates="reservation")
