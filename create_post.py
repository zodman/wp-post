import requests
import click
from jinja2 import Environment, select_autoescape
import jinja2
from conf import URL_BASE,  AUTH_BASIC
from plugins import mal

env = Environment(loader=jinja2.FileSystemLoader("."),
                  autoescape=select_autoescape())


@click.command()
@click.option("--mal-id", required=True, type=int)
@click.option("--title", required=True, type=str)
@click.option("--status",
              required=True,
              type=click.Choice(
                  "publish, future, draft, pending, private".split(", ")))
@click.option("--template", default="index.html")
def create_post(mal_id, title, status, template):
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
                         headers={'Authorization': f"Basic {AUTH_BASIC}"})
    entry = resp.json()
    print(f"{entry['id']} {entry['status']} | {entry['title']['rendered']} {entry['link']}")


if __name__ == "__main__":
    create_post()
