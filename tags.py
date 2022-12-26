import click
import requests
from slugify import slugify
from rich import print
from conf import URL_BASE, headers
from jinja2 import Environment, select_autoescape
import jinja2

env = Environment(loader=jinja2.FileSystemLoader("."),
                  autoescape=select_autoescape())


def _render(entry):
    print(f"{entry['id']} | {entry['name']} {entry['link']}")


@click.group()
def tag():
    pass


@tag.command()
@click.argument("tag_id")
@click.argument("name")
@click.argument("slug")
def edit(tag_id, name, slug):
    url = f"{URL_BASE}wp/v2/tags/{tag_id}"
    data = {'name': name, 'slug': slug, 'id': tag_id}
    response = requests.post(url, data=data, headers=headers)

    data = response.json()
    _render(data)


@tag.command()
@click.argument("name")
def create(name):

    url = f"{URL_BASE}wp/v2/tags"
    data = {'name': name, 'slug': slugify(name)}
    response = requests.post(url, data=data, headers=headers)

    data = response.json()
    for entry in data:
        _render(entry)


@tag.command()
def list():
    url = f"{URL_BASE}wp/v2/tags"
    response = requests.get(url, headers=headers)
    data = response.json()
    for entry in data:
        _render(entry)


if __name__ == "__main__":
    tag()
