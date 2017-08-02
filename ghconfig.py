import click
import requests
import os


# Get GitHub token from environment variable
GH_TOKEN = os.environ.get('GH_TOKEN')
API_BASE_URL = 'https://api.github.com'


def search_repositories(organisation, name):
    headers = {'Authorization': 'Token {0}'.format(GH_TOKEN)}
    api_url = '{0}/orgs/{1}/repos'.format(API_BASE_URL, organisation)
    response = requests.get(api_url, headers=headers)

    repositories = []

    if response.status_code == 200:
        repositories = response.json()

        while response.links.get('next') is not None:
            print('Processing: {0}'.format(response.links['next']['url']))
            response = requests.get(
                response.links['next']['url'], headers=headers)
            repositories += response.json()

    print('Total {0} repositories: {1}'.format(
        organisation, len(repositories)))

    repositories_found = []

    for repo in repositories:
        if name in repo['name']:
            repositories_found.append(repo)

    return repositories_found


@click.command()
def check_config():
    print('Checking GitHub configuration...')
    repos = search_repositories('alphagov', 'paas-')
    print('Found {0} repositories'.format(len(repos)))


if __name__ == '__main__':
    check_config()
