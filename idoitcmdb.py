# -*- coding: utf-8 -*-
import subprocess
from errbot import BotPlugin, botcmd
import cmdb


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
        result = cmdb.search(str(args))
        return cmdb.searchformatter(result)

    @botcmd
    def cmdb_nets(self, msg, args):
        """ Netzwerk Suche """
        return search(str(args), filter='Net')

    @botcmd
    def cmdb_show (self, msg, args):
        """ Objektdetailansicht """
        return cmdb.clirun('show', str(args))[1]

    @botcmd
    def cmdb_nextip(self, msg, args):
        """ Nächste freie IP in einem Netzwerk """
        return cmdb.clirun('nextip', str(args))[1]

    @botcmd
    def cmdb_read(self, msg, args):
       """ Kategorienübersicht """
       if args:
            return cmdb.clirun('read', str(args))[1]
       else:
            return cmdb.clirun('read')[1]
