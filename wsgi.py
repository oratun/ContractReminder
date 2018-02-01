
import sys
from os.path import abspath
from os.path import dirname
from manage import app


sys.path.insert(0, abspath(dirname(__file__)))
application = app

"""
建立一个软连接
ln -s /var/www/ContractReminder/cr.conf /etc/supervisor/conf.d/cr.conf

ln -s /var/www/ContractReminder/cr.nginx /etc/nginx/sites-enabled/cr



➜  ~ cat /etc/supervisor/conf.d/cr.conf

[program:bbs]
command=/usr/local/bin/gunicorn wsgi -c gunicorn.config.py
directory=/var/www/cr
autostart=true
autorestart=true




/usr/local/bin/gunicorn wsgi
--bind 0.0.0.0:5001
--pid /tmp/cr.pid
"""
