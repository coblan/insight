# -*-encoding:utf-8 -*-
"""
sync webcode with first

Usage:
    python sync_webcode.py
    
"""
from __future__ import unicode_literals
import sys
import os
sys.path.append(r'D:\coblan\py2')
from heTools.sync_code import sync

#import wingdbstub

tp = ('port.py','db_tools.py')
def func(src,dst):
    if src.endswith('.pyc'):
        return False
    #if src.endswith(tp):
        #return True
    else:
        return True

dc={
    'dirs':[(ur'D:\coblan\webcode\helpers',ur'D:\coblan\web\insight\src\helpers'),
            (ur'D:\coblan\webcode\res',ur'D:\coblan\web\insight\src\static\res'),],
    'include_file':func,
    }

if __name__=='__main__':
    sync(dc)