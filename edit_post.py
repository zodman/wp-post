import requests
import click
from jinja2 import Environment, select_autoescape
import jinja2
from conf import URL_BASE, AUTH_BASIC

env = Environment(loader=jinja2.FileSystemLoader("."),
                  autoescape=select_autoescape())


@click.command()
@click.argument('post_id')
@click.option("--mal-id", required=False, type=int)
@click.option("--title", required=True, type=str)
@click.option("--status",
              required=True,
              type=click.Choice(
                  "publish, future, draft, pending, private".split(", ")))
@click.option("--template", default="index.html")
def edit_post(post_id, mal_id, title, status, template):
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
        pass

    html_content = template.render(context)

    url = f"{URL_BASE}wp/v2/posts/{post_id}"
    resp = requests.post(url,
                         data={
                             'title': title,
                             'status': status,
                             'content': html_content,
                         },
                         headers={'Authorization': f"Basic {AUTH_BASIC}"})
    entry = resp.json()
    print(f"{entry['id']} {entry['status']} | {entry['title']['rendered']}"
          f"{entry['link']}")


if __name__ == "__main__":
    edit_post()
