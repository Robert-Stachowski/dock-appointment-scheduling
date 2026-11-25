from enum import StrEnum


class AccountRole(StrEnum):
    ADMIN = "admin"
    WAREHOUSEMAN = "warehouseman"
    CARRIER = "carrier"
    SYSTEM = "system"


class ReservationStatus(StrEnum):
    PENDING = "pending"
    LATE = "late"
    AFTER_HOURS_PAID = "after_hours_paid"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LogEventType(StrEnum):
    CREATED = "created"
    DATA_CHANGED = "data_changed"
    STATUS_CHANGED = "status_changed"
    CANCELLED = "cancelled"
