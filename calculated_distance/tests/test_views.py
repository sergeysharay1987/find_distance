from werkzeug.test import Client

from werkzeug.testapp import test_app

c = Client(test_app)

response = c.get("/")




response.status_code
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
