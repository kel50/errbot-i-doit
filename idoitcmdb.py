# -*- coding: utf-8 -*-
import subprocess
from errbot import BotPlugin, botcmd

IDOITCLI = 'idoitcli --no-colors'

class CMDB(BotPlugin):

#    @botcmd
#    def cmdb(self, msg, args):
#        #output = u'[Markdown]: http://google.com *bold*'
#        output = u'<http://google.com|Link>'
        #return output
#        return "```\n{output}\n```".format(output=output)

    @botcmd
    def cmdb_search(self, msg, args):
        """ CMDB Suche """
        #self.send(msg.frm, str(args))
        return search(str(args))

    @botcmd
    def cmdb_nets(self, msg, args):
        """ Netzwerk Suche """
        return search(str(args), filter='Net')

    @botcmd
    def cmdb_show (self, msg, args):
        """ Objektdetailansicht """
        return clirun('show', str(args))[1]

    @botcmd
    def cmdb_nextip(self, msg, args):
        """ Nächste freie IP in einem Netzwerk """
        return clirun('nextip', str(args))[1]

    @botcmd
    def cmdb_read(self, msg, args):
       """ Kategorienübersicht """
       if args:
            return clirun('read', str(args))[1]
       else:
            return clirun('read')[1]



def clirun(command, arguments=None):
        if arguments == '':
            return 'Was soll ich denn damit anfangen? :man-facepalming: Da musst du schon mehr eingeben ...'
        elif arguments is None: 
            runCMD = ' '.join([IDOITCLI, command])
        else:
            runCMD = ' '.join([IDOITCLI, command, arguments])
        out = subprocess.Popen(runCMD, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (stdout, stderr) = out.communicate()
        rc = out.returncode
        if rc > 0:
            return rc, 'Da ist wohl was schief gelaufen: ```' + stderr.strip().decode() + '```'
        else:
            return rc, stdout.strip().decode()
        

def search(term, filter=None):
        if term == '':
            return 'Was soll ich denn damit anfangen? :man-facepalming: Da musst du schon mehr eingeben ...'
        searchCMD = 'search {}'.format(term)
        if filter == 'Net':
            searchCMD = 'search {}|grep -A2 -B1 "Source: Layer 3\-Net"|grep -v "\-\-"'.format(term)
        rc, out = clirun(searchCMD)
        if rc > 0:
            return out
        else:
            if out.split('\n\n')[0] == '':
                return 'Keine Suchergebnisse für _{}_'.format(term)
            itemlist = [i.split('\n') for i in out.split('\n\n')]  # get single lines for every search result item
            items = [{'name': i[0], 'place':i[1].replace('Source: ', ''), 'url': i[2].replace('Link: ', '')} for i in itemlist]  # save information to dict and remove description in text
            return '\n'.join(["```\n<{url}|{name}> ({place})\n```".format(**item) for item in items])
