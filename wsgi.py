
import os
from app import create_app


application = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    application.run()
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
