# -*- coding: utf-8 -*-

""" module to run idoitcli commands via python """

import subprocess

IDOITCLI = 'idoitcli --no-colors -y'


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

