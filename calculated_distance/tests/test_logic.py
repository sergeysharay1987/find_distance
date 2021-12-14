import pytest
from calculated_distance.logic import *


# def test_geocode_address(address):

@pytest.fixture(params=['Russia Luhovitsy',
                        'Russia Ryazan',
                        'Belarus'])
def get_distance(request):
    coords_addr = geocode_address(request.param)
    coords_addr = Point(coords_addr)
    return find_distance(coords_addr)


def test_find_distance(get_distance):

    assert isinstance(get_distance, float)

