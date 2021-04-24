from dataclasses import dataclass, astuple, asdict, field
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
        
            error_code = ''
            if not -90 <= self.lat <= 90:
                error_code += f"Latitude must be in [-90; 90]: passed {self.lat}\n"
            if not -180 <= self.lng <= 180:
                error_code += f"Longitude must be in [-180; 180]: passed {self.lng}\n"
            if error_code:
                raise ValueError(error_code[-1])
            

@dataclass
class Address:
    """Class for keeping track of an users adress"""
    street: str
    suite: str
    city: str
    zipcode: str
    geo: GeoPoint = field(repr=asdict)

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
    address: Address = field(repr=asdict)
    phone: str
    website: str
    company: dict

    def __post_init__(self):
        if isinstance(self.address, dict):
            self.address = Address(**self.address)

    def geo(self) -> tuple[float]:
        return astuple(self.address.geo)