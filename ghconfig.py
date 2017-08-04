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


def set_branch_protection(organisation, repository, branch):
    headers = {
        'Authorization': 'Token {0}'.format(GH_TOKEN),
        'Accept': 'application/vnd.github.loki-preview+json'
    }

    api_url = '{0}/repos/{1}/{2}/branches/{3}/protection'.format(
        API_BASE_URL, organisation, repository, branch)

    payload = {
        "required_status_checks": None,
        "required_pull_request_reviews": None,
        "enforce_admins": True,
        "restrictions": None
    }

    response = requests.put(api_url, headers=headers, json=payload)
    return response.status_code, response.json()


def remove_branch_protection(organisation, repository, branch):
    headers = {
        'Authorization': 'Token {0}'.format(GH_TOKEN),
        'Accept': 'application/vnd.github.loki-preview+json'
    }

    api_url = '{0}/repos/{1}/{2}/branches/{3}/protection'.format(
        API_BASE_URL, organisation, repository, branch)

    response = requests.delete(api_url, headers=headers)
    return response.status_code


@click.option(
    '--organisation', help='Name of the Organisation or GitHub user.',
    default='alphagov')
@click.option(
    '--filter', help='Specify a filter for repository names (example: paas-',
    default='')
@click.command()
def check_config(organisation, filter):
    print('Checking GitHub configuration...')

    # Filter repositories to work on using the specified organisation and
    # repository names filter
    repos = search_repositories(organisation, filter)


if __name__ == '__main__':
    check_config()
