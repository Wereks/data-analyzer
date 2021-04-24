from dataclasses import asdict

import pytest

from main.classes import *

@pytest.mark.parametrize('lat, lng',
                        [
                            ('-90', '-180'), 
                            ('-90', '180'),
                            ('-90', '0'),
                            ('90', '180'),
                            ('90', '-180'),
                            ('90', '0'),
                            ('0','0')
                        ])
def test_geo_correct(lat, lng):
    point = GeoPoint(lat, lng)
    assert astuple(point) == (float(lat), float(lng))

@pytest.mark.parametrize('lat, lng',
                        [
                            ('-89.5345212', '-179.421562'), 
                            ('-89.3', '179.345234'),
                            ('-89.9999999', '0.123456'),
                            ('89.33333333', '179.23245'),
                            ('89.999999998', '-179.234'),
                            ('89.99993', '0'),
                            ('0','0')
                        ])
def test_geo_correct_rounding(lat, lng):
    point = GeoPoint(lat, lng)
    lat = round(float(lat), 6)
    lng = round(float(lng), 6)
    assert astuple(point) == (lat, lng)

@pytest.mark.parametrize('lat, lng',
                        [
                            ('-90.000001', '-180.001'), 
                            ('-90', '180.1'),
                            ('-91', '0'),
                            ('90.3', '180'),
                            ('90', '-250'),
                            ('91', '0')
                        ])
def test_geo_incorrent(lat, lng):
    with pytest.raises(ValueError):
        GeoPoint(lat, lng)

def test_address(local_users):
    json_ = local_users('example')
    for user_dict in json_:
        address_dict = user_dict['address']
        geo = address_dict['geo']
        geo['lat'] = round(float(geo['lat'] ), 6)
        geo['lng'] = round(float(geo['lng'] ), 6)
        address = Address(**address_dict)
        assert sorted(address_dict.items()) == sorted(asdict(address).items())

def test_user(local_users):
    json_ = local_users('example')
    for user_dict in json_:
        geo = user_dict['address']['geo']
        geo['lat'] = round(float(geo['lat'] ), 6)
        geo['lng'] = round(float(geo['lng'] ), 6)
        user = User(**user_dict)
        assert sorted(user_dict.items()) == sorted(asdict(user).items())

def test_post(local_posts):
    json_ = local_posts('example')
    for post_dict in json_:
        post = Post(**post_dict)
        assert sorted(post_dict.items()) == sorted(post._asdict().items())