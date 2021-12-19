import os

import pytest
from geopy import Location

from calculated_distance.logic import *

dir_to_shape_file: str = os.getcwd() + '/' + blueprint
path_to_blueprint = os.getcwd()


@pytest.fixture(params=['Russia Luhovitsy',
                        'Russia Ryazan',
                        'Belarus'])
def get_distance(request):
    location: Location = ya_geocoder.geocode(request.param)
    print(location)
    # coords_addr = get_location(request.param)
    coords_addr = Point(location.latitude, location.longitude)
    return find_distance(coords_addr)


def test_read_shp_file():
    print(os.chdir())


def test_find_distance(get_distance):
    assert isinstance(get_distance, float)
