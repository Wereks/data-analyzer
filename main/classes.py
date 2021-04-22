from dataclasses import dataclass, astuple
from collections import namedtuple
from typing import Union, ClassVar

Post = namedtuple('Post', 'userId id title body')

@dataclass
class GeoPoint:
    """Class for keeping track of an users geolocation"""
    lat: float
    lng: float

    def __post_init__(self):
            self.lat = round(float(self.lat), 6)
            self.lng = round(float(self.lng), 6)
            if not -90 <= self.lat <= 90:
                raise ValueError("Latitude must be in [-90; 90]")
            if not -180 <= self.lng <= 180:
                raise ValueError("Longtitude must be in [-180; 180]")

@dataclass
class Address:
    """Class for keeping track of an users adress"""
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoPoint

    def __post_init__(self):
        if isinstance(self.geo, dict):
            self.geo = GeoPoint(**self.geo)

@dataclass
class User:
    """Class for keeping track of an user"""
    id: str
    name: str
    username: str
    email: str
    address: Address
    phone: str
    website: str
    company: dict

    def __post_init__(self):
        if isinstance(self.address, dict):
            self.address = Address(**self.address)

    def geo(self) -> tuple[float]:
        return astuple(self.address.geo)