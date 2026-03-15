"""Shared PostgreSQL types (enums and structured fields)."""

from __future__ import annotations

from enum import Enum
from datetime import datetime
from sqlalchemy import Enum as SAEnum


# ----- Enum definitions -----


class AccountType(str, Enum):
    ADMIN = "admin"
    COMPANY = "company"
    TRUCK_DRIVER = "driver"


class OrderStatus(str, Enum):
    PENDING = "pending"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class VehicleType(str, Enum):
    T3_5 = "3.5t"
    T7_5 = "7.5t"
    T12 = "12t"
    T18 = "18t"
    T40 = "40t"
    FIXED_BODY = "fixed_body"
    ARTICULATED_TRAILER = "articulated_trailer"
    TRAILER = "trailer"
    OTHER = "other"


class Currency(str, Enum):
    EUR = "EUR"
    BAM = "BAM"
    BGN = "BGN"
    CZK = "CZK"
    HUF = "HUF"
    ISK = "ISK"
    KZT = "KZT"
    MKD = "MKD"
    MDL = "MDL"
    PLN = "PLN"
    RON = "RON"
    RUB = "RUB"
    RSD = "RSD"
    SEK = "SEK"
    CHF = "CHF"
    TRY = "TRY"
    UAH = "UAH"
    BYN = "BYN"
    USD = "USD"
    HRK = "HRK"
    DKK = "DKK"
    NOK = "NOK"


class WorkScheduleType(str, Enum):
    COMEBACK = "comeback"
    FULL_WEEK = "full-week"


class WorkScheduleStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"


class ScheduleSource(str, Enum):
    MANUAL = "manual"
    IMPORT = "import"
    OPTIMIZER = "optimizer"
    MIXED = "mixed"


class SolutionStatus(str, Enum):
    UNKNOWN = "UNKNOWN"
    MODEL_INVALID = "MODEL_INVALID"
    INFEASIBLE = "INFEASIBLE"
    FEASIBLE = "FEASIBLE"
    OPTIMAL = "OPTIMAL"


class documentType(str, Enum):
    BUSINESS_ACTIVITY_LICENSE = "business_activity_license"
    GOODS_INSURANCE = "goods_insurance"
    LIABILITY_INSURANCE = "liability_insurance"
    TRANSPORT_AUTHORIZATION_CARD = "transport_authorization_card"
    NATIONAL_ID_CARD = "national_id_card"
    VEHICLE_REGISTRATION_CERTIFICATE = "vehicle_registration_certificate"
    VEHICLE_TECHNICAL_INSPECTION_CERTIFICATE = "vehicle_technical_inspection_certificate"
    DRIVING_LICENSE = "driving_license"


class documentStatus(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


# ----- Structured fields (composite types) -----

class VehicleStatus(str, Enum):
    WAITING = "waiting"
    UNDER_MAINTENANCE = "under_maintenance"
    TO_PICKUP = "to_pickup"
    ON_DELIVERY = "on_delivery"
    RETURNING = "returning"
    OUT_OF_SERVICE = "out_of_service"

class PositionType:
    name: str
    country: str
    city: str
    address: str
    coordinates: tuple[float, float]
    postcode: str

    def __init__(
        self,
        name: str,
        country: str,
        city: str,
        address: str,
        coordinates: tuple[float, float],
        postcode: str,
    ):
        self.name = name
        self.country = country
        self.city = city
        self.address = address
        self.coordinates = coordinates
        self.postcode = postcode

    def __composite_values__(self):
        return (
            self.name,
            self.country,
            self.city,
            self.address,
            self.coordinates,
            self.postcode,
        )

    def __repr__(self):
        return f"PositionType({self.city}, {self.address})"

    def __eq__(self, other):
        return (
            isinstance(other, PositionType)
            and self.__composite_values__() == other.__composite_values__()
        )


class TimeWindowType:
    start: datetime  # aquí mapeamos 'from' a 'start', no usar palabra reservada 'from'
    end: datetime

    def __init__(self, start: datetime, end: datetime):
        self.start = start
        self.end = end

    def __composite_values__(self):
        return (self.start, self.end)

    def __repr__(self):
        return f"TimeWindow(start={self.start}, end={self.end})"

    def __eq__(self, other):
        return (
            isinstance(other, TimeWindowType)
            and self.start == other.start
            and self.end == other.end
        )


# Export SQLAlchemy Enum helpers for reuse
AccountTypeEnum = SAEnum(AccountType, name="account_type")
OrderStatusEnum = SAEnum(OrderStatus, name="order_status")
VehicleTypeEnum = SAEnum(VehicleType, name="vehicle_type")
CurrencyEnum = SAEnum(Currency, name="currency")
WorkScheduleTypeEnum = SAEnum(WorkScheduleType, name="work_schedule_type")
WorkScheduleStatusEnum = SAEnum(WorkScheduleStatus, name="work_schedule_status")
ScheduleSourceEnum = SAEnum(ScheduleSource, name="schedule_source")
SolutionStatusEnum = SAEnum(SolutionStatus, name="solution_status")
DocumentTypeEnum = SAEnum(documentType, name="document_type")
DocumentStatusEnum = SAEnum(documentStatus, name="document_status")
VehicleStatusEnum = SAEnum(VehicleStatus, name="vehicle_status")
