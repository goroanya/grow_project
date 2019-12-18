import socket
import os
import getpass
import sys
import subprocess

# Cleaning for not the first run
os.system('systemctl kill server')
os.system('systemctl kill client')
FILES_TO_DELETE = ['server.sock',
                   'client.sock',
                   '/etc/systemd/system/server.service',
                   '/etc/systemd/system/client.service',
                   '/etc/nginx/sites-available/server',
                   '/etc/nginx/sites-available/client']
for file in FILES_TO_DELETE:
    try:
        os.remove(file)
    except OSError:
        pass

os.system('sudo unlink /etc/nginx/sites-enabled/server')
os.system('sudo unlink /etc/nginx/sites-enabled/client')
SERVICE_DESCRIPTION = '''
[Unit]
Description=$DESCRIPTION
After=network.target

[Service]
User=$USERNAME
Group=www-data
WorkingDirectory=$CWD
Environment="PATH=$EXECUTABLE"
ExecStart=$GUNICORN_PATH --log-file $CWD/$NAME.log --log-level debug --bind unix:$CWD/$NAME.sock -m 007 $MODULE_NAME:APP

[Install]
WantedBy=multi-user.target'''

SERVER_SOCKET_PATH = 'server.sock'
CLIENT_SOCKET_PATH = 'client.sock'
USERNAME = getpass.getuser()
CWD = os.getcwd()
EXECUTABLE_PYTHON_DIR = '/'.join(sys.executable.split('/')[:-1])
GUNICORN_PATH = subprocess.check_output(['whereis', 'gunicorn']).decode('utf-8').split(' ')[1].strip()

# Creating sockets
socket.socket(socket.AF_UNIX).bind(SERVER_SOCKET_PATH)
socket.socket(socket.AF_UNIX).bind(CLIENT_SOCKET_PATH)
print('Sockets created')

data = SERVICE_DESCRIPTION \
    .replace('$USERNAME', USERNAME) \
    .replace('$GUNICORN_PATH', GUNICORN_PATH) \
    .replace('$EXECUTABLE', EXECUTABLE_PYTHON_DIR) \
    .replace('$CWD', CWD) \
    .replace('$DESCRIPTION', 'Server service') \
    .replace('$NAME', 'server') \
    .replace('$MODULE_NAME', 'rest')
os.system(f'sudo sh -c \'printf "{data}" > /etc/systemd/system/server.service\'')

data = SERVICE_DESCRIPTION \
        .replace('$USERNAME', USERNAME) \
        .replace('$GUNICORN_PATH', GUNICORN_PATH) \
        .replace('$EXECUTABLE', EXECUTABLE_PYTHON_DIR) \
        .replace('$CWD', CWD) \
        .replace('$DESCRIPTION', 'Client service') \
        .replace('$NAME', 'client') \
        .replace('$MODULE_NAME', 'views')
os.system(f'sudo sh -c \'printf "{data}" > /etc/systemd/system/client.service\'')
print('Service information written')

NGINX_DESCRIPTION = '''
upstream $NAME {
  server unix:$CWD/$NAME.sock fail_timeout=0;
}
server {
    listen 80;
    server_name $NAME.test;

    location / {
        root $CWD/;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header Host \$http_host;
        proxy_redirect off;
        if (!-f \$request_filename) {
            proxy_pass http://$NAME;
            break;
        }
    }
    location /static/ {
        root $CWD/;
        try_files \$uri \$uri/ =404;
    }
}
'''

data = NGINX_DESCRIPTION.replace('$CWD', CWD).replace('$NAME', 'server')
os.system(f'sudo sh -c \'printf "{data}" > /etc/nginx/sites-available/server\'')
data = NGINX_DESCRIPTION.replace('$CWD', CWD).replace('$NAME', 'client')
os.system(f'sudo sh -c \'printf "{data}" > /etc/nginx/sites-available/client\'')

HOSTS_LINE = '127.0.0.1 client.test server.test'
with open('/etc/hosts', 'r') as f:
    data = f.read()
    if HOSTS_LINE not in data:
        os.system(f'sudo sh -c \'printf "\n{HOSTS_LINE}\n" >>  /etc/hosts\'')

print('NGINX information written')
os.system('sudo ln -s /etc/nginx/sites-available/server /etc/nginx/sites-enabled')
os.system('sudo ln -s /etc/nginx/sites-available/client /etc/nginx/sites-enabled')
os.system('systemctl daemon-reload')
os.system('systemctl restart nginx')
print('Nginx service are configured')