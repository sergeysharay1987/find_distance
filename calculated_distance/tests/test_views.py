import pytest
from django.core.management import call_command
from django.test.client import Client
from web_calculator.settings import BASE_DIR
from calculator.views import *
# from pytest_django.asserts

# define variable containing names of context's keys in views.py
_keys_of_context_using_in_views = ['form', 'expression', 'expressions', 'expression']


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        call_command('loaddata', BASE_DIR +'/db_for_tests.json')


@pytest.fixture(params=[reverse('details', kwargs={'id': 100}),  # /calculator/database/100/
                        reverse('delete', kwargs={'id': 35}),  # /calculator/database/35/delete/
                        reverse('database'),  # /calculator/database
                        reverse('index')])  # /calculator/
def make_response(request):
    path = request.param
    client = Client()
    response = client.get(path)
    return response


def get_id_from_path(path):
    id_from_path = path.split('/')
    id = id_from_path[-2]
    return id


@pytest.mark.django_db()
def test_path():
    path = reverse('details', kwargs={'id': 1})

    # id = get_id_from_path(path)
    # exp_details = Expression.objects.get(id=id)
    client = Client()
    response = client.get(path)
    print(response.context.keys())
    # print(path)
    # print(id_from_path)
    # print(exp_details)
    # print(response.context)


@pytest.fixture()
def key_of_context(make_response):
    context_list = make_response.context
    keys = context_list.keys()
    for key in keys:

        if key in _keys_of_context_using_in_views:
            return key


@pytest.mark.django_db
def test_key_of_context(make_response):
    content = make_response.content
    context_list = make_response.context
    #print(context_list)
    keys = context_list.keys()
    print(keys)
    for key in keys:

        if key in _keys_of_context_using_in_views:
            return key


@pytest.fixture()
def template(make_response):
    """Return content of template"""
    templates_using_in_views = make_response.templates
    for template in templates_using_in_views:
        content_template_file = open(BASE_DIR + f'/calculator/templates/{template.name}', 'r').read()
        return content_template_file


@pytest.mark.django_db
def test_equality_key_of_context_using_in_template_with_key_using_in_views(template, key_of_context):
    """Check if key of context in views.py equals key using in template"""
    assert key_of_context in template
