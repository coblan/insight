import multiprocessing
import os
bind = '127.0.0.1:10100'
workers = multiprocessing.cpu_count() * 2 + 1
backlog = 2048
#worker_class = "sync"
worker_class = 'gevent'
debug = True
proc_name = 'insight'
pidfile = '/pypro/{proc_name}/run/{proc_name}.pid'.format(proc_name=proc_name)
#logfile = '/pypro/mysite/log/debug.log'
accesslog='/pypro/{proc_name}/log/{proc_name}.log'.format(proc_name=proc_name)
errorlog='/pypro/{proc_name}/log/{proc_name}_error.log'.format(proc_name=proc_name)
loglevel = 'debug'
chdir = '/pypro/{proc_name}/src'.format(proc_name=proc_name)
timeout=60

#stdout_logfile='/pypro/mysite/log/mysite_std.log'
#stderr_logfile='/pypro/mysite/log/mysite_std.log'
#gunicorn -c gunicorn.py.ini wsgi:application