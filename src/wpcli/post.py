import click
import requests
from rich import print
import jinja2
from jinja2 import Environment, select_autoescape, ChainableUndefined
from slugify import slugify
from .conf import URL_BASE, headers
from .plugins import mal, deepl, tmdb

env = Environment(loader=jinja2.FileSystemLoader("."),
                  autoescape=select_autoescape(),
                  undefined=ChainableUndefined)
env.filters['translate'] = deepl.translate
env.filters['retranslate'] = deepl.retranslate
env.filters['img'] = lambda x: x.replace('https://', 'https://i0.wp.com/')
env.filters['tmdb_img'] = lambda x: ''.join([
    'https://image.tmdb.org/t/p/original/', x
]).replace('https://', 'https://i0.wp.com/')


def _render(entry):
    print(f"{entry['id']} {entry['status']} | {entry['title']['rendered']} | "
          f"{entry['link']} cats:{entry['categories']} tags: {entry['tags']}")


def _create_data(**kwargs):
    data = {
        'slug': kwargs.get("slug"),
        'status': kwargs.get("status"),
        'content': kwargs.get('content'),
    }
    title = kwargs.get('title')
    if title:
        data['title'] = title
    category = kwargs.get('category')
    if category:
        data['categories'] = category
    tag = kwargs.get('category')
    if tag:
        data['tags'] = tag
    return data


@click.group()
def post():
    pass


@post.command()
@click.option("--status",
              default='publish',
              type=click.Choice(
                  "publish, future, draft, pending, private".split(", ")))
def list(status):
    url = f"{URL_BASE}wp/v2/posts"
    data = dict(status=status)
    resp = requests.get(url, params=data, headers=headers)
    if not resp.ok:
        print(resp.json())
    data = resp.json()

    for entry in data:
        _render(entry)


@post.command()
@click.argument('post_id')
@click.option("--mal-id", type=int)
@click.option("--title", type=str)
@click.option("--slug", type=str)
@click.option("--status",
              default='publish',
              type=click.Choice(
                  "publish, future, draft, pending, private".split(", ")))
@click.option("--category", multiple=True, help="multiple", type=int)
@click.option("--tag", multiple=True, help='multiple', type=int)
@click.option("--template", default="index.html")
@click.option("--tmdb-id-movie")
@click.option("--tmdb-id-tv")
def edit(post_id, mal_id, title, slug, status, category, tag, template,
         tmdb_id_movie, tmdb_id_tv):
    context = {}
    template_obj = env.get_template(template)

    if mal_id:
        context["mal"] = mal.fetch(mal_id)

    if tmdb_id_movie:
        result = tmdb.fetch_movie(tmdb_id_movie)
        context['tmdb_movie'] = result

    if tmdb_id_tv:
        result = tmdb.fetch_tv(tmdb_id_tv)
        context['tmdb_tv'] = result

    content = template_obj.render(context)
    url = f"{URL_BASE}wp/v2/posts/{post_id}"
    if not slug and title:
        slug = slugify(title)

    data = _create_data(title=title,
                        slug=slug,
                        category=category,
                        tag=tag,
                        content=content)
    resp = requests.post(url, data=data, headers=headers)
    if resp.ok:
        entry = resp.json()
        _render(entry)
    else:
        print(resp.text)


@post.command()
@click.option("--mal-id", required=True, type=int)
@click.option("--title", required=True, type=str)
@click.option("--status",
              required=True,
              type=click.Choice(
                  "publish, future, draft, pending, private".split(", ")))
@click.option("--template", default="index.html")
@click.option("--category", multiple=True, help="multiple", type=int)
@click.option("--tag", multiple=True, help='multiple', type=int)
@click.option("--tmdb-id-movie")
@click.option("--tmdb-id-tv")
def create(mal_id, title, status, template, category, tag, tmdb_id_tv,
           tmdb_id_movie):
    context = {}
    if mal_id:
        context["mal"] = mal.fetch(mal_id)

    if tmdb_id_movie:
        result = tmdb.fetch_movie(tmdb_id_movie)
        context['tmdb_movie'] = result

    if tmdb_id_tv:
        result = tmdb.fetch_tv(tmdb_id_tv)
        context['tmdb_tv'] = result

    template_instance = env.get_template(template)
    html_content = template_instance.render(context)
    url = f"{URL_BASE}wp/v2/posts"
    data = _create_data(title=title,
                        category=category,
                        tag=tag,
                        content=html_content)

    resp = requests.post(url, data=data, headers=headers)
    entry = resp.json()
    if not resp.ok:
        print(entry)

    _render(entry)


if __name__ == "__main__":
    post()
