import os
import subprocess
from flask import Blueprint
import click
from app.models import Post

bp = Blueprint('cli', __name__, cli_group=None)


@bp.cli.command()
def reindex():
    """Reindex all posts in Elasticsearch."""
    Post.reindex()
    click.echo('Reindexed all posts.')


@bp.cli.group()
def translate():
    """Translation and localization commands."""
    pass


@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    subprocess.run(['pybabel', 'extract', '-F', 'babel.cfg', '-k', '_l', '-o', 'messages.pot', '.'], check=True)
    subprocess.run(['pybabel', 'init', '-i', 'messages.pot', '-d', 'app/translations', '-l', lang], check=True)
    os.remove('messages.pot')


@translate.command()
def update():
    """Update all languages."""
    subprocess.run(['pybabel', 'extract', '-F', 'babel.cfg', '-k', '_l', '-o', 'messages.pot', '.'], check=True)
    subprocess.run(['pybabel', 'update', '-i', 'messages.pot', '-d', 'app/translations'], check=True)
    os.remove('messages.pot')


@translate.command()
def compile():
    """Compile all languages."""
    subprocess.run(['pybabel', 'compile', '-d', 'app/translations'], check=True)