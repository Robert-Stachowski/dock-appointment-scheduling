from sqlalchemy import Identity, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Ramp(Base):
    __tablename__ = "ramps"

    id: Mapped[int] = mapped_column(Identity(), primary_key=True)
    name: Mapped[str] = mapped_column(String(20), unique=True)

    def __repr__(self) -> str:
        return f"Rampa: {self.id} - {self.name}"
