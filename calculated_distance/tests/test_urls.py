from django.urls import reverse, resolve
import pytest


@pytest.mark.parametrize('view_name', ['index', 'database', 'details', 'delete'])
def test_path_of_page(view_name):

    if view_name == 'details' or view_name == 'delete':
        path = reverse(view_name, kwargs={'id': 5})
    else:
        path = reverse(view_name)
    assert resolve(path).view_name == view_name

