import responses
from ghconfig import search_repositories
import json


@responses.activate
def test_search_repositories():
    first_header = {'Link': (
        '<https://api.github.com/organizations/596977/repos?page=2>;'
        'rel="next",'
        '<https://api.github.com/organizations/596977/repos?page=22>;'
        'rel="last"')}

    first_body = [
        {'name': 'invalid-1'},
        {'name': 'invalid-2'},
        {'name': 'paas-foo'},
        {'name': 'invalid-3'},
        {'name': 'paas-bar'}
    ]

    second_body = [
        {'name': 'invalid-4'},
        {'name': 'invalid-5'},
        {'name': 'paas-baz'},
        {'name': 'invalid-6'},
        {'name': 'paas-boo'}
    ]

    responses.add(
        responses.GET, 'https://api.github.com/orgs/alphagov/repos',
        body=json.dumps(first_body), status=200,
        content_type='application/json',
        headers=first_header)

    responses.add(
        responses.GET,
        'https://api.github.com/organizations/596977/repos?page=2',
        body=json.dumps(second_body), status=200,
        content_type='application/json')

    repositories = search_repositories('alphagov', 'paas-')
    assert len(repositories) == 4