import click
import requests
from rich import print
from conf import URL_BASE, headers
import jinja2
from jinja2 import Environment, select_autoescape
import re
from plugins import mal
from slugify import slugify


env = Environment(loader=jinja2.FileSystemLoader("."),
                  autoescape=select_autoescape())


def _render(entry):
    print(f"{entry['id']} {entry['status']} | {entry['title']['rendered']} "
          f"{entry['link']}")


@click.group()
def post():
    pass


@post.command()
def list():
    url = f"{URL_BASE}wp/v2/posts"
    resp = requests.get(url, headers=headers)
    data = resp.json()
    for entry in data:
        print(f"{entry['id']} {entry['status']} | {entry['title']['rendered']}"
              f"{entry['link']}")

        content = entry['content']['rendered']
        regex_string = '\<\!\-\-\ args\:\ \ (?P<args>.*)\ \ \-\-\>'
        r = re.search(regex_string, content)
        if r:
            print(r.group('args'))


@post.command()
@click.argument('post_id')
@click.option("--mal-id", required=False, type=int)
@click.option("--title", required=True, type=str)
@click.option("--slug",type=str)
@click.option("--status",
              default='publish',
              type=click.Choice(
                  "publish, future, draft, pending, private".split(", ")))
@click.option("--template", default="index.html")
def edit(post_id, mal_id, title, slug, status, template):
    context = {
        '_args': {
            '--mal_id': mal_id,
            '--title': title,
            '--status': status,
            '--template': template
        }
    }
    template_obj = env.get_template(template)

    if mal_id:
        context["mal"] = mal.fetch(mal_id)

    html_content = template_obj.render(context)
    url = f"{URL_BASE}wp/v2/posts/{post_id}"
    slug = slug or slugify(title)
    resp = requests.post(url,
                         data={
                             'title': title,
                             'slug': slug,
                             'status': status,
                             'content': html_content,
                         },
                         headers=headers)
    entry = resp.json()
    _render(entry)


@post.command()
@click.option("--mal-id", required=True, type=int)
@click.option("--title", required=True, type=str)
@click.option("--status",
              required=True,
              type=click.Choice(
                  "publish, future, draft, pending, private".split(", ")))
@click.option("--template", default="index.html")
def create(mal_id, title, status, template):
    context = {
        '_args': {
            '--mal_id': mal_id,
            '--title': title,
            '--status': status,
            '--template': template
        }
    }
    template = env.get_template(template)
    if mal_id:
        context["mal"] = mal.fetch(mal_id)
    html_content = template.render(context)

    url = f"{URL_BASE}wp/v2/posts"
    resp = requests.post(url,
                         data={
                             'title': title,
                             'status': status,
                             'content': html_content,
                         },
                         headers=headers)
    entry = resp.json()
    _render(entry)


if __name__ == "__main__":
    post()
