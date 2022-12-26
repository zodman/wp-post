import click
import requests
from slugify import slugify
from rich import print
from conf import URL_BASE, headers


@click.group()
def tag():
    pass


@tag.command()
@click.argument("name")
def create(name):

    url = f"{URL_BASE}wp/v2/tags"
    data = {'name': name, 'slug': slugify(name)}
    response = requests.post(url, data=data, headers=headers)

    data = response.json()
    for entry in data:
        print(
            f"{entry['id']} | {entry['name']} {entry['slug']} {entry['link']}")


@tag.command()
def list():

    url = f"{URL_BASE}wp/v2/tags"
    response = requests.get(url, headers=headers)
    data = response.json()
    for entry in data:
        print(
            f"{entry['id']} | {entry['name']} {entry['slug']} {entry['link']}")


if __name__ == "__main__":
    tag()
