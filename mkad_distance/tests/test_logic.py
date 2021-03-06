import pytest
from geopy import Location
from mkad_distance.logic import Point, ya_geocoder, find_distance
from mkad_distance.blueprint import poly_mkad


@pytest.fixture(params=['Russia Luhovitsy',
                        'Russia Ryazan',
                        'Belarus'])
def get_distance(request):
    location: Location = ya_geocoder.geocode(request.param)
    coords_addr = Point(location.latitude, location.longitude)
    return find_distance(coords_addr, poly_mkad)


def test_find_distance(get_distance):
    assert isinstance(get_distance, (float, int))
