"""Daily Bread application."""

import datetime
import os
import random

import requests
from bottle import TEMPLATE_PATH, route, run, static_file, template

from cache import cache
from config import BIBLESEARCH_API_KEY


__all__ = ['index', 'server_static']

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
BIBLE_VERSION = 'eng-KJV'
TEMPLATE_PATH.insert(0, os.path.join(BASE_PATH, 'templates'))


def _get_all_books_w_chaps():
    """Returns Bible Search API JSON of all books and chapters.

    :returns: JSON of all books with chapter numbers
    :rtype: dict[str, str]

    """
    url = (f'https://bibles.org/v2/versions/{BIBLE_VERSION}/books.js'
           f'?include_chapters=true')
    return requests.get(url, auth=(BIBLESEARCH_API_KEY, '')).json()


def _get_random_book(resp):
    """Returns a random bible book.

    :param resp: Bible Search API JSON of books and chapters
    :type resp: dict[str, str]
    :returns: JSON of random book
    :rtype: dict[str, str]

    """
    return random.choice(resp['response']['books'])


def _get_random_chapter(book_json):
    """Returns a random bible chapter number.

    :param book_json: JSON of random book
    :type book_json: dict[str, str]
    :returns: random chapter number
    :rtype: str

    """
    return random.choice(book_json['chapters'])['chapter']


def _get_bible_text(book_abbr, chap):
    """Returns the bible text of the specified book and chapter.

    :param book_abbr: abbreviation of book title
    :type book_abbr: str
    :param chap: chapter number
    :type chap: str
    :returns: bible text with FUMS (Fair Use Management System)
    :rtype: str

    """
    url = (f'https://bibles.org/v2/passages.js'
           f'?q[]={book_abbr}+{chap}&version={BIBLE_VERSION}')
    resp = requests.get(url, auth=(BIBLESEARCH_API_KEY, '')).json()
    return '\n'.join([
        resp['response']['search']['result']['passages'][0]['text'],
        resp['response']['meta']['fums']
    ])


@route('/')
def index():
    """Returns the index page."""
    date_today = datetime.date.today().toordinal()
    if 'current_date' not in cache or cache['current_date'] != date_today:
        random.seed(date_today)
        book_json = _get_random_book(_get_all_books_w_chaps())
        chap = _get_random_chapter(book_json)
        cache['current_date'] = date_today
        cache['title'] = f"{book_json['name']} {chap}"
        cache['text'] = _get_bible_text(book_json['abbr'], chap)
        cache['copyright'] = book_json['copyright']
    return template(
        'index',
        title=cache['title'],
        text=cache['text'],
        copyright=cache['copyright']
    )


@route('/static/<filepath:path>')
def server_static(filepath):
    """Returns all assets."""
    return static_file(filepath, root=os.path.join(BASE_PATH, 'static'))


if __name__ == '__main__':
    run()
