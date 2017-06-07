# encoding:utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
from helpers.director.shortcut import page_dc
from helpers.director import kv


class MHome(object):
    template='wx/home.html'
    need_login=False
    def __init__(self,request):
        self.request=request
    
    def get_context(self):
        return {}


    
class Help(object):
    def get_context(self):
        ctx={
            'help_text':kv.get_value('help_text','')
        }        
        return ctx


page_dc.update({
    'home.wx':MHome,
    'help.wx':help,
})