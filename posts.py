import click
import requests
from rich import print
from conf import URL_BASE,  AUTH_BASIC
import re


@click.command()
def posts():
    url = f"{URL_BASE}wp/v2/posts"
    resp = requests.get(url,
                         headers={
                             'Authorization': f"Basic {AUTH_BASIC}"})
    data = resp.json()
    for entry in data:
        print(f"{entry['id']} {entry['status']} | {entry['title']['rendered']}"
              f"{entry['link']}")

        content = entry['content']['rendered']
        r = re.search('\<\!\-\-\ args\:\ \ (?P<args>.*)\ \ \-\-\>', content)
        if r:
            print(r.group('args'))


if __name__ == "__main__":
    posts()
