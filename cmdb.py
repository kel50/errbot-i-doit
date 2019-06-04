# -*- coding: utf-8 -*-
import subprocess

IDOITCLI = 'idoitcli --no-colors -y'
RELEVANT_FIELDS = ['Title', 'ID', 'Type', 'CMDB status', 'Created', 'Updated', 'E-mail address', 'Last change by', 'Function', 'Personnel number', 'Telephone company', 'Cellphone', 'Department', 'Description']


def clirun(command, arguments=None):
        if arguments == '':
            return 'Was soll ich denn damit anfangen? :man-facepalming: Da musst du schon mehr eingeben ...'
        elif arguments is None: 
            runCMD = ' '.join([IDOITCLI, command])
        else:
            runCMD = '{} {} "{}"'.format(IDOITCLI, command, arguments)
        out = subprocess.Popen(runCMD, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = out.communicate()
        rc = out.returncode
        if rc > 0:
            return rc, 'Da ist wohl was schief gelaufen: ```' + stderr.strip().decode() + '```'
        else:
            return rc, stdout.strip().decode()
        

def search(term, filter=None):
        if term == '':
            return None
        searchCMD = 'search "{}"'.format(term)
        if filter == 'Net':
            searchCMD = 'search "{}"|grep -A2 -B1 "Source: Layer 3\-Net"|grep -v "\-\-"'.format(term)
        rc, out = clirun(searchCMD)
        return out


def searchformatter(objectliststring):
        if objectliststring.split('\n\n')[0] == '':
            return 'Keine Ergebnisse'
        itemlist = [i.split('\n') for i in objectliststring.split('\n\n')]  # get single lines for every search result item
        items = [{'name': i[0], 'place':i[1].replace('Source: ', ''), 'url': i[2].replace('Link: ', '')} for i in itemlist]  # save information to dict and remove description in text
        return '\n'.join(["```\n<{url}|{name}> ({place})\n```".format(**item) for item in items])


def nonemptyformatter(infostring):
        lines = infostring.split('\n')
        result = []
        for line in lines:
            if not line.endswith(': -'):
                result.append(line)
        return '\n'.join(result)


def relevantformatter(infostring):
        lines = infostring.split('\n')
        result = []
        for line in lines:
            if line.split(':')[0] in RELEVANT_FIELDS and line not in result:
                result.append(line)
        return '\n'.join(result)
        

