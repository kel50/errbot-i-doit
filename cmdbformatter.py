def searchformatter(objectliststring):
    """ format search result with links """
    if objectliststring.split('\n\n')[0] == '':
        return 'Keine Ergebnisse'
    itemlist = [i.split('\n') for i in objectliststring.split('\n\n')]  # get single lines for every search result item
    items = [{'name': i[0], 'place':i[1].replace('Source: ', ''), 'url': i[2].replace('Link: ', '')} for i in itemlist]  # save information to dict and remove description in text
    return '\n'.join(["```\n<{url}|{name}> ({place})\n```".format(**item) for item in items])


def nonemptyformatter(infostring):
    """ return only fields with content for show output """
    lines = infostring.split('\n')
    result = []
    for line in lines:
        if not line.endswith(': -'):
            result.append(line)
    return '\n'.join(result)


def relevantformatter(infostring):
    """ return only relevant fields for show output """
    lines = infostring.split('\n')
    result = []
    for line in lines:
        if line.split(':')[0] in RELEVANT_FIELDS and line not in result:
            result.append(line)
    return '\n'.join(result)
