from typing import TYPE_CHECKING

from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.reservation import Reservation


class Ramp(Base):
    __tablename__ = "ramps"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="ramp")

    def __repr__(self) -> str:
        return f"Rampa: {self.id} - {self.name}"
