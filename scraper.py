import json
import re

from mwclient import Site


def GetCards():
    with open('wiki-credentials.json', 'r') as f:
        credentials = json.load(f)
    site = Site('wiki.dominionstrategy.com', scheme='http', path='/')
    site.login(credentials['username'], credentials['password'])

    page = site.pages['List_of_cards']
    pageText = page.text()
