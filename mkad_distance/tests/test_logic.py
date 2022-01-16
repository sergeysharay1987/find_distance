import pytest
from flask import url_for, get_flashed_messages, Flask
from geopy import Location

from config import Configuration
from mkad_distance.logic import Point, ya_geocoder, find_distance
from mkad_distance.blueprint import poly_mkad, mkad_distance
from app import application


@pytest.fixture(autouse=True)
def create_app():
    from app import application
    application.config['TESTING'] = True
    application.app_context().push()
    application.test_request_context().push()
    return application


def test_url():

    #with application.app_context():
    #print(f'application.app_context(): {application.app_context()}')
    assert '/calculate_distance/' == url_for('mkad_distance.index')


@pytest.fixture(params=['Russia Luhovitsy',
                        'Russia Ryazan',
                        'Belarus',
                        '0'])
#def get_distance(request):
def coords(request):
    location: Location = ya_geocoder.geocode(request.param)
    coords_addr = Point(location.latitude, location.longitude)
    return coords_addr
    #return find_distance(coords_addr, poly_mkad)


@pytest.mark.xfail
def test_find_distance(coords):
    print(coords)
    #assert isinstance(get_distance, (float, int))
    distance = find_distance(coords, poly_mkad)
    if not isinstance(distance, (float, int)):
        assert get_flashed_messages()
        print(get_flashed_messages())
    assert isinstance(distance, (float, int))



def test_blueprint():
    client = application.test_client()
    #with application.test_request_context():
    response = client.post(url_for('mkad_distance.index'), data={'address': '-'})
    session = client.session_transaction()
    print(get_flashed_messages())
    print(response)


def test_flash_messages():
    client = application.test_client()

    with client.session_transaction() as session:
        res = client.post(url_for('mkad_distance.index'), data={'address': '0'})
        print(f'get_flashed_messages(with_categories=True): {get_flashed_messages()}')
        print(res.data.decode())
        print(session)
