import click
from rich import print


@click.command()
def help():
    print('[bold cyan]For execute: ')
    print('python -m wpcli.post --help')
    print('python -m wpcli.tag --help')
    print('python -m wpcli.cat --help')


if __name__ == "__main__":
    help()
