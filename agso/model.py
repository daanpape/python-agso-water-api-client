from typing import NamedTuple
from datetime import datetime

class AgsoAddress(NamedTuple):
    street: str
    number: str
    municipality: str
    zipcode: str
    country: str
    building_name: str
    description: str


class AgsoMeter(NamedTuple):
    max_unit: int
    meter_number: int


class AgsoSubscriber(NamedTuple):
    customer_number: int
    subscriber_number: str
    first_name: str
    last_name: str
    home_address: AgsoAddress
    billing_address: AgsoAddress
    email: str
    fax: str
    mobile: str
    phone: str
    meters: list[AgsoMeter]


class AgsoValue(NamedTuple):
    time: datetime
    value: float
    estimation: bool
