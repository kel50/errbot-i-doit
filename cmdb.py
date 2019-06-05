# -*- coding: utf-8 -*-

""" module to run idoitcli commands via python """

import subprocess

IDOITCLI = 'idoitcli --no-colors -y'
RELEVANT_FIELDS = ['Title', 'ID', 'Type', 'CMDB status', 'Created', 'Updated', 'E-mail address', 'Last change by', 'Function', 'Personnel number', 'Telephone company', 'Cellphone', 'Department', 'Description']


def clirun(command, arguments=None):
    """ run idoitcli with optional arguments """
    if arguments == '':
        return 'Was soll ich denn damit anfangen? :man-facepalming: Da musst du schon mehr eingeben ...'
    elif arguments is None:
        run_cmd = ' '.join([IDOITCLI, command])
    else:
        run_cmd = '{} {} "{}"'.format(IDOITCLI, command, arguments)
    out = subprocess.Popen(run_cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = out.communicate()
    return_code = out.returncode
    if return_code > 0:
        return return_code, 'Da ist wohl was schief gelaufen: ```' + stderr.strip().decode() + '```'
    else:
        return return_code, stdout.strip().decode()


def search(term, search_filter=None):
    """ search for term, optionally filter for networks """
    if term == '':
        return None
    search_cmd = 'search "{}"'.format(term)
    if search_filter == 'Net':
        search_cmd = 'search "{}"|grep -A2 -B1 "Source: Layer 3\-Net"|grep -v "\-\-"'.format(term)
    out = clirun(search_cmd)[1]
    return out


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
