import click
import requests
from slugify import slugify
from rich import print
from conf import URL_BASE, headers


def _render(entry):
    print(f"{entry['id']} | {entry['name']} {entry['link']}")


@click.group()
def category():
    pass


@category.command()
@click.argument("category_id")
@click.argument("name")
@click.argument("slug")
def edit(category_id, name, slug):
    url = f"{URL_BASE}wp/v2/categories/{category_id}"
    data = {'name': name, 'slug': slug, 'id': category_id}
    response = requests.post(url, data=data, headers=headers)

    data = response.json()
    _render(data)


@category.command()
@click.argument("name")
def create(name):

    url = f"{URL_BASE}wp/v2/categories"
    data = {'name': name, 'slug': slugify(name)}
    response = requests.post(url, data=data, headers=headers)
    data = response.json()
    print(data)
    _render(data)


@category.command()
def list():
    url = f"{URL_BASE}wp/v2/categories"
    response = requests.get(url, headers=headers)
    data = response.json()
    for entry in data:
        _render(entry)


if __name__ == "__main__":
    category()
