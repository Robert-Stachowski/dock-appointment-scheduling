from enum import StrEnum


class AccountRole(StrEnum):
    ADMIN = "admin"
    WAREHOUSEMAN = "warehouseman"
    CARRIER = "carrier"
    SYSTEM = "system"
