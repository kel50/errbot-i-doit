# -*- coding: utf-8 -*-
import subprocess
from errbot import BotPlugin, botcmd
import cmdb
from cmdbformatter import searchformatter, nonemptyformatter, relevantformatter, codeformatter


class CMDB(BotPlugin):

#    @botcmd
#    def cmdb(self, msg, args):
#        #output = u'[Markdown]: http://google.com *bold*'
#        output = u'<http://google.com|Link>'
        #return output
#        return "```\n{output}\n```".format(output=output)

    @botcmd
    def cmdb_search(self, msg, args):
        """ CMDB search """
        result = cmdb.search(str(args))
        return searchformatter(result)

    @botcmd
    def cmdb_nets(self, msg, args):
        """ CMDB network search """
        return cmdb.search(str(args), search_filter='Net')

    @botcmd
    def cmdb_show (self, msg, args):
        """ CMDB object view """
        result = cmdb.clirun('show', str(args))[1]
        return relevantformatter(result)

    @botcmd
    def cmdb_show_v(self, msg, args):
        """ CMDB object detail view """
        result = cmdb.clirun('show', str(args))[1]
        return nonemptyformatter(result)

    @botcmd
    def cmdb_nextip(self, msg, args):
        """ CMDB next free IP address """
        return cmdb.clirun('nextip', str(args))[1]

    @botcmd
    def cmdb_read(self, msg, args):
       """ CMDB category overview """
       if args:
            return cmdb.clirun('read', str(args))[1]
       else:
            return cmdb.clirun('read')[1]

    @botcmd
    def cmdb_rack(self, msg, args):
        """ CMDB rack view """
        result = cmdb.clirun('rack', str(args))[1]
        return codeformatter(result)

    @botcmd
    def cmdb_network(self, msg, args):
        """ CMDB network view """
        result = cmdb.clirun('network', str(args))[1]
        return codeformatter(result)

    @botcmd(split_args_with=',')
    def cmdb_newserver(self, msg, args):
        """ create new server with name, location, IP in your CMDB"""
        name, location, ip = args
        cmdb.clirun('save',  'server/{}'.format(name))
        cmdb.clirun('save server/{}/location -a location=\"{}\"'.format(name.strip(), location.strip()))
        cmdb.clirun('save \"server/{}/Host address\" -a \"IPv4 address\"=\"{}\"'.format(name.strip(), ip.strip()))
        yield 'idoitcli save \"server/{}/Host address\" -a \"IPv4 address\"=\"{}\"'.format(name.strip(), ip.strip())
        result = cmdb.search(name)
        yield searchformatter(result)
#        yield cmdb.clirun('read \"server/{}/Host address\"'.format(name.strip()))[1]
        yield nonemptyformatter(cmdb.clirun('read \"server/{}/location\"'.format(name.strip()))[1])
