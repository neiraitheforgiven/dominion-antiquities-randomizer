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
    rows = pageText.split('\n|-\n')
    cards = []

    # Parse Header
    #   The first row will have the declaration of the table and some
    #   descriptive text and will end with the table header row. The table
    #   header will begin with "! "
    headerRow = rows[0].splitlines()[-1][2:]
    header = re.split(r' *!! *', headerRow)

    # Fix last row
    #   Trim everything after the table
    lastRow = rows.pop().splitlines()
    for i, line in enumerate(lastRow):
        if line.startswith('|}'):
            break
    lastRow = '\n'.join(lastRow[:i])
    rows.append(lastRow)

    # Process rows
    for row in rows[1:]:
        columns = re.split(r' *\|\| *', row)
        if len(columns) < len(header):
            for x in range(len(header) - len(columns)):
                columns.append('')
        cards.append(dict(zip(header, columns)))

    return cards
