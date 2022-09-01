import requests
import click
import pprint
from jinja2 import Environment, select_autoescape
import jinja2

URL_BASE = "http://localhost/wp-json/"
JIKAN_URL = "https://api.jikan.moe/v4/anime/{0}/full"
AUTH_BASIC = "YWRtaW46YWRtaW4="

env = Environment(loader=jinja2.FileSystemLoader("."),
                  autoescape=select_autoescape())


@click.command()
@click.option("--mal-id", required=True, type=int)
@click.option("--title", required=True, type=str)
@click.option("--status", required=True, type=click.Choice("publish, future, draft, pending, private".split(", ")))
@click.option("--template", default="index.html")
def posts(mal_id, title, status, template):
    template = env.get_template(template)
    context = {}

    url = JIKAN_URL.format(mal_id)
    resp = requests.get(url)

    mal_data = resp.json().get("data")

    if not mal_data:
        click.echo("mal_id not found")
        return
    context["mal"] = mal_data
    html_content = template.render(context)

    url = f"{URL_BASE}wp/v2/posts"
    resp = requests.post(url,
                         data={
                             'title': title,
                             'status': status,
                             'content': html_content,
                         },
                         headers={'Authorization': f"Basic {AUTH_BASIC}"})
    pprint.pp(resp.json())


if __name__ == "__main__":
    posts()
